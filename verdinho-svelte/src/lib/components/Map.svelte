<script lang="ts">
	import type { Map, Rectangle, LatLngBoundsExpression, LeafletEventHandlerFn } from 'leaflet';
	import { mapState, type QuadrantBounds, type QuadrantData } from '$lib/stores/mapStore.svelte';
	import { getRecommendedPlant } from '../../services/http/get-recommended-plant';
	import { quadrantModalStore } from '@/stores/quadrant-modal-store.svelte';
	let mapContainer: HTMLElement | null = $state(null);
	let map: Map | null = $state(null);
	// We need to use any because of how we dynamically import Leaflet

	let L: typeof import('leaflet');

	// const OWM_API_KEY = 'ed5dbe9896c14fb2526e2c777a124718';
	const SQUARE_SIZE = $state(0.005);

	const popupClasses = () => ({
		header: `bg-[#FF0000]! py-2! px-3! rounded-t-md! -mx-3! -mt-2! mb-3! font-bold! text-center!`,
		body: 'text-sm! leading-relaxed!',
		row: 'mb-2! flex! items-center!',
		icon: 'min-w-6! text-center! mr-2!',
		label: 'font-semibold!',
		value: 'ml-1!'
	});

	$effect(() => {
		const createMap = async () => {
			// Dynamically import Leaflet only on client side
			const leaflet = await import('leaflet');
			L = leaflet.default;

			// Import the CSS
			await import('leaflet/dist/leaflet.css');

			// Import Leaflet Draw plugin
			await import('leaflet-draw/dist/leaflet.draw.css');
			await import('leaflet-draw');

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
					map.addLayer(mapState.drawnItems);

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

	async function generateQuadrants(latMin: number, lonMin: number, latMax: number, lonMax: number) {
		if (!map || !L) return;

		const stepsLat = getSteps(latMin, latMax, SQUARE_SIZE);
		const stepsLon = getSteps(lonMin, lonMax, SQUARE_SIZE);
		const BATCH_SIZE = 2; // Process quadrants one at a time to avoid overwhelming the APIs
		const toProcessQuadrants: QuadrantBounds[] = [];

		// Add all processing quadrants before starting the batches
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
					toProcessQuadrants.push(quadrantBounds);
				}
			}
		}

		// Process quadrants in batches to avoid overwhelming the backend
		for (let i = 0; i < toProcessQuadrants.length; i += BATCH_SIZE) {
			const batch = toProcessQuadrants.slice(i, i + BATCH_SIZE);
			const batchPromises = batch.map(async (quadrant) => {
				const recommendedPlantForArea = await getRecommendedPlant({
					latMin: quadrant.latMin,
					lonMin: quadrant.lonMin,
					latMax: quadrant.latMax,
					lonMax: quadrant.lonMax
				});

				if (recommendedPlantForArea) {
					// Create quadrant data for store
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

					// Add prediction data to popup
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

					// Add features data to popup
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

					mapState.removeProcessingQuadrant(quadrant);

					return {
						bounds: [
							[quadrant.latMin, quadrant.lonMin],
							[quadrant.latMax, quadrant.lonMax]
						] as LatLngBoundsExpression,
						color: 'oklch(79.2% 0.209 151.711)',
						popup: bodyWrapper,
						latitude: quadrant.latMin,
						longitude: quadrant.lonMin,
						predition: recommendedPlantForArea.prediction,
						features_used: recommendedPlantForArea.features_used
					};
				}
				return null;
			});

			// Wait for current batch to resolve
			const results = await Promise.all(batchPromises);

			// Add valid results to the map
			results.forEach((result) => {
				if (result && map && L) {
					L.rectangle(result.bounds, {
						color: result.color,
						weight: 1,
						fillOpacity: 0.6
					})
						.on('click', () => {
							const quadrantData: QuadrantData = {
								lat: result.latitude,
								lon: result.longitude,
								quadrantBounds: {
									latMin: result.bounds[0][0],
									lonMin: result.bounds[0][1],
									latMax: result.bounds[1][0],
									lonMax: result.bounds[1][1]
								},
								analyzedAreaData: result.features_used,
								plantRecommendation: result.predition
							};

							quadrantModalStore.updateQuadrant(quadrantData);
							quadrantModalStore.openModal();
						})
						.addTo(map);
				}
			});
		}

		// Set lastAnalyzedArea with timestamp
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

	$inspect(mapState.processingQuadrants);
</script>

<div bind:this={mapContainer} class="map"></div>

<style>
	.map {
		width: 100%;
		height: 100vh;
	}
</style>
