<script lang="ts">
	import type { Map, Rectangle, LeafletEventHandlerFn } from 'leaflet';
	import { mapState, type QuadrantData } from '$lib/stores/mapStore.svelte';
	import { getRecommendedPlant } from '../../services/http/get-recommended-plant';
	import { quadrantModalStore } from '@/stores/quadrant-modal-store.svelte';
	let mapContainer: HTMLElement | null = $state(null);
	let map: Map | null = $state(null);
	// We need to use any because of how we dynamically import Leaflet

	let L: typeof import('leaflet');

	const SQUARE_SIZE = 0.005;

	const popupClasses = () => ({
		header: `bg-[#FF0000]! py-2! px-3! rounded-t-md! -mx-3! -mt-2! mb-3! font-bold! text-center!`,
		body: 'text-sm! leading-relaxed!',
		row: 'mb-2! flex! items-center!',
		icon: 'min-w-6! text-center! mr-2!',
		label: 'font-semibold!',
		value: 'ml-1!'
	});

	let isProcessingQuadrant = $state(false);

	$effect(() => {
		const createMap = async () => {
			// Dynamically import Leaflet only on client side
			const [leaflet] = await Promise.all([
				await import('leaflet'),
				// Import the CSS
				import('leaflet/dist/leaflet.css'),
				// Import Leaflet Draw plugin
				import('leaflet-draw/dist/leaflet.draw.css'),
				import('leaflet-draw')
			]);

			L = leaflet.default;

			// Fix the "type is not defined" error by defining the missing readableArea function
			if (L.GeometryUtil) {
				// Make sure readableArea has the necessary type parameter by implementing it directly
				L.GeometryUtil.readableArea = function (area, isMetric, precision) {
					// This variable is needed by other parts of the leaflet-draw code
					if (isMetric) {
						if (area >= 10000) {
							return L.GeometryUtil.formattedNumber(String(area * 0.0001), precision) + ' ha';
						} else {
							return L.GeometryUtil.formattedNumber(String(area), precision) + ' m²';
						}
					} else {
						const acres = area * 0.00024711;
						if (acres >= 1) {
							return L.GeometryUtil.formattedNumber(String(acres), precision) + ' acres';
						} else {
							return L.GeometryUtil.formattedNumber(String(area), precision) + ' ft²';
						}
					}
				};
			}

			if (L.drawLocal && L.drawLocal.draw && L.drawLocal.draw.handlers) {
				L.drawLocal.draw.handlers.rectangle = {
					tooltip: {
						start: 'Clique e arraste para desenhar uma área.'
					}
				};

				L.drawLocal.draw.toolbar.buttons.rectangle = 'Desenhar um retângulo';
				L.drawLocal.draw.handlers.simpleshape.tooltip.end = 'Solte para finalizar';
				L.drawLocal.draw.toolbar.actions.title = 'Cancelar desenho';
				L.drawLocal.draw.toolbar.actions.text = 'Cancelar';
				L.drawLocal.draw.toolbar.finish.title = 'Finalizar desenho';
				L.drawLocal.draw.toolbar.finish.text = 'Finalizar';
				L.drawLocal.draw.toolbar.undo.title = 'Desfazer última alteração';
				L.drawLocal.draw.toolbar.undo.text = 'Desfazer';

				L.drawLocal.edit = {
					toolbar: {
						actions: {
							save: {
								title: 'Salvar alterações',
								text: 'Salvar'
							},
							cancel: {
								title: 'Cancelar edição, descartando todas as alterações',
								text: 'Cancelar'
							},
							clearAll: {
								title: 'Limpar todos os desenhos',
								text: 'Limpar Tudo'
							}
						},
						buttons: {
							edit: 'Editar desenhos',
							editDisabled: 'Sem desenhos para editar',
							remove: 'Excluir desenhos',
							removeDisabled: 'Sem desenhos para excluir'
						}
					},
					handlers: {
						edit: {
							tooltip: {
								text: 'Arraste os pontos ou marcadores para editar.',
								subtext: 'Clique cancelar para desfazer as alterações.'
							}
						},
						remove: {
							tooltip: {
								text: 'Clique em um desenho para remover'
							}
						}
					}
				};
			}

			// Initialize map once L is available
			if (mapContainer && L) {
				map = L.map(mapContainer).setView([-22.9505, -43.3804], 14);

				L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
					attribution: '© OpenStreetMap contributors'
				}).addTo(map);

				// Initialize draw controls
				mapState.drawnItems = new L.FeatureGroup();
				if (map && mapState.drawnItems) {
					(map as Map).addLayer(mapState.drawnItems);

					const drawControl = new L.Control.Draw({
						draw: {
							polygon: false,
							marker: false,
							polyline: false,
							circle: false,
							circlemarker: false,
							rectangle: {
								shapeOptions: {
									color: 'oklch(44.8% 0.119 151.328)',
									weight: 2,
									opacity: 0.5
								},
								metric: true
							}
						}
						// edit: { featureGroup: drawnItems }
					});

					map.addControl(drawControl);

					// Handle map events
					map.on('draw:created', (async (event: { layer: Rectangle }) => {
						console.log('Draw Created');
						const layer = event.layer;
						if (mapState.drawnItems) {
							// mapState.drawnItems.clearLayers();
							mapState.drawnItems.addLayer(layer);
						}

						const bounds = layer.getBounds();
						// Snap bounds to grid
						const latMin = Math.floor(bounds.getSouthWest().lat / SQUARE_SIZE) * SQUARE_SIZE;
						const lonMin = Math.floor(bounds.getSouthWest().lng / SQUARE_SIZE) * SQUARE_SIZE;
						const latMax = Math.ceil(bounds.getNorthEast().lat / SQUARE_SIZE) * SQUARE_SIZE;
						const lonMax = Math.ceil(bounds.getNorthEast().lng / SQUARE_SIZE) * SQUARE_SIZE;

						layer.setBounds([
							[latMin, lonMin],
							[latMax, lonMax]
						]);

						// Update store with selected area
						mapState.selectedArea = { latMin, lonMin, latMax, lonMax };

						generateQuadrants(latMin, lonMin, latMax, lonMax);
					}) as LeafletEventHandlerFn);

					// NEW: Generate quadrants for visible map bounds on moveend
					// map.on('moveend', async () => {
					// 	if (!map) return;
					// 	const bounds = map.getBounds();
					// 	const latMin = bounds.getSouthWest().lat;
					// 	const lonMin = bounds.getSouthWest().lng;
					// 	const latMax = bounds.getNorthEast().lat;
					// 	const lonMax = bounds.getNorthEast().lng;

					// 	// Optionally update selectedArea to reflect visible area
					// 	mapState.selectedArea = { latMin, lonMin, latMax, lonMax };

					//  generateQuadrants(latMin, lonMin, latMax, lonMax);
					// });
				}
			}
		};

		createMap();

		return () => {
			if (map) map.remove();
		};
	});

	// Helper to handle floating point imprecision
	function getSteps(min: number, max: number, size: number) {
		const diff = max - min;
		const steps = diff / size;
		if (Math.abs(Math.round(steps) - steps) < 1e-8) {
			return Math.round(steps);
		}
		return Math.ceil(steps);
	}

	$effect(() => {
		if (!map) return;

		const BATCH_SIZE = 2;
		if (!isProcessingQuadrant && mapState.processingQuadrants.length > 0 && L) {
			isProcessingQuadrant = true;
			const batch = mapState.processingQuadrants.slice(0, BATCH_SIZE);
			const processBatch = async () => {
				await Promise.all(
					batch.map(async (quadrant) => {
						if (!map) return;
						try {
							const recommendedPlantForArea = await getRecommendedPlant({
								latMin: quadrant.latMin,
								lonMin: quadrant.lonMin,
								latMax: quadrant.latMax,
								lonMax: quadrant.lonMax
							});

							if (recommendedPlantForArea) {
								const quadrantData: QuadrantData = {
									lat: quadrant.latMin,
									lon: quadrant.lonMin,
									quadrantBounds: quadrant,
									plantRecommendation: recommendedPlantForArea.prediction,
									analyzedAreaData: recommendedPlantForArea.features_used
								};
								mapState.addQuadrant(quadrantData);

								const popup = popupClasses();
								const bodyWrapper = document.createElement('div');
								bodyWrapper.classList.add(...popup.body.split(' '));

								for (const key in recommendedPlantForArea.prediction) {
									const rowWrapper = document.createElement('div');
									rowWrapper.classList.add(...popup.row.split(' '));
									const icon = document.createElement('span');
									icon.classList.add(...popup.icon.split(' '));
									const label = document.createElement('strong');
									label.classList.add(...popup.label.split(' '));
									const value = document.createElement('span');
									value.classList.add(...popup.value.split(' '));
									value.textContent = `${key}: ${recommendedPlantForArea.prediction[key as keyof typeof recommendedPlantForArea.prediction]}`;
									rowWrapper.appendChild(icon);
									rowWrapper.appendChild(label);
									rowWrapper.appendChild(value);
									bodyWrapper.appendChild(rowWrapper);
								}
								for (const key in recommendedPlantForArea.features_used) {
									const rowWrapper = document.createElement('div');
									rowWrapper.classList.add(...popup.row.split(' '));
									const icon = document.createElement('span');
									icon.classList.add(...popup.icon.split(' '));
									const label = document.createElement('strong');
									label.classList.add(...popup.label.split(' '));
									const value = document.createElement('span');
									value.classList.add(...popup.value.split(' '));
									value.textContent = `${key}: ${recommendedPlantForArea.features_used[key as keyof typeof recommendedPlantForArea.features_used]}`;
									rowWrapper.appendChild(icon);
									rowWrapper.appendChild(label);
									rowWrapper.appendChild(value);
									bodyWrapper.appendChild(rowWrapper);
								}

								const openQuadrantModal = () => {
									const quadrantData: QuadrantData = {
										lat: quadrant.latMin,
										lon: quadrant.lonMin,
										quadrantBounds: quadrant,
										analyzedAreaData: recommendedPlantForArea.features_used,
										plantRecommendation: recommendedPlantForArea.prediction
									};
									quadrantModalStore.updateQuadrant(quadrantData);
									quadrantModalStore.openModal();
								};

								L.rectangle(
									[
										[quadrant.latMin, quadrant.lonMin],
										[quadrant.latMax, quadrant.lonMax]
									],
									{
										color: 'oklch(79.2% 0.209 151.711)',
										weight: 1,
										fillOpacity: 0.6
									}
								)
									.on('click', openQuadrantModal)
									.addTo(map);

								// Add a marker with the scientific name at the center of the rectangle
								const centerLat = (quadrant.latMin + quadrant.latMax) / 2;
								const centerLon = (quadrant.lonMin + quadrant.lonMax) / 2;
								const scientificName = recommendedPlantForArea.prediction.cientific_name || '';
								const scientificNameWrapper = document.createElement('div');
								bodyWrapper.appendChild(scientificNameWrapper);
								L.marker([centerLat, centerLon], {
									icon: L.divIcon({
										html: (() => {
											const div = document.createElement('div');
											div.className =
												'bg-white/80 rounded-md px-2 py-0.5 text-xs font-bold text-green-800 border border-green-200 shadow-sm text-center';
											div.textContent = scientificName;
											return div.outerHTML;
										})(),
										className: '',
										iconSize: [120, 24],
										iconAnchor: [60, 12]
									})
								})
									.on('dblclick', openQuadrantModal)
									.on('click', () => {
										if (!map) return;

										map.setView([centerLat, centerLon], 15);
									})
									.addTo(map as Map);
							}
						} catch (e) {
							console.error('Error processing quadrant:', e);
						} finally {
							mapState.removeProcessingQuadrant(quadrant);
						}
					})
				);
				isProcessingQuadrant = false;
			};
			processBatch();
		}
	});

	async function generateQuadrants(latMin: number, lonMin: number, latMax: number, lonMax: number) {
		if (!map || !L) return;

		const stepsLat = getSteps(latMin, latMax, SQUARE_SIZE);
		const stepsLon = getSteps(lonMin, lonMax, SQUARE_SIZE);

		for (let i = 0; i < stepsLat; i++) {
			for (let j = 0; j < stepsLon; j++) {
				const lat = latMin + i * SQUARE_SIZE;
				const lon = lonMin + j * SQUARE_SIZE;

				const quadrantBounds = {
					latMin: lat,
					lonMin: lon,
					latMax: lat + SQUARE_SIZE,
					lonMax: lon + SQUARE_SIZE
				};

				if (!mapState.hasQuadrantWithSameArea(quadrantBounds)) {
					mapState.addProcessingQuadrant(quadrantBounds);
				}
			}
		}

		mapState.lastAnalyzedArea = {
			latMin,
			lonMin,
			latMax,
			lonMax,
			timestamp: Date.now()
		};
	}

	$effect(() => {
		if (!mapState.isProcessing) {
			mapState.clearDrawings();
		}
	});
</script>

<div bind:this={mapContainer} class="map"></div>

<style>
	.map {
		width: 100%;
		height: 100vh;
	}
</style>
