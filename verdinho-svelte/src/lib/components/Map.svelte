<script lang="ts">
	import type {
		Map,
		FeatureGroup,
		Rectangle,
		LatLngBoundsExpression,
		LeafletEventHandlerFn
	} from 'leaflet';
	import { mapState, type QuadrantData } from '$lib/stores/mapStore.svelte';
	import { getRecommendedPlant } from '../../services/http/get-recommended-plant';

	let mapContainer: HTMLElement | null = $state(null);
	let map: Map | null = $state(null);
	let drawnItems: FeatureGroup | null = $state(null);
	// We need to use any because of how we dynamically import Leaflet

	let L: typeof import('leaflet');

	// const OWM_API_KEY = 'ed5dbe9896c14fb2526e2c777a124718';
	const SQUARE_SIZE = $state(0.005);

	const popupClasses = () => ({
		header: `!bg-[#FF0000] !py-2 !px-3 !rounded-t-md !-mx-3 !-mt-2 !mb-3 !font-bold !text-center`,
		body: '!text-sm !leading-relaxed',
		row: '!mb-2 !flex !items-center',
		icon: '!min-w-6 !text-center !mr-2',
		label: '!font-semibold',
		value: '!ml-1'
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
					const type = isMetric ? 'metric' : 'imperial';

					// Use the type in a console log to prevent "unused variable" warning
					// This is important as other parts of the code rely on this variable existing
					if (window.console && window.console.debug) {
						window.console.debug(`Area displayed in ${type} units`);
					}

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
				drawnItems = new L.FeatureGroup();
				if (map && drawnItems) {
					map.addLayer(drawnItems);

					const drawControl = new L.Control.Draw({
						draw: {
							polygon: false,
							marker: false,
							polyline: false,
							circle: false,
							circlemarker: false,
							rectangle: {
								shapeOptions: {
									color: 'red',
									weight: 2,
									opacity: 0.5
								},
								metric: true
							}
						},
						edit: { featureGroup: drawnItems }
					});

					map.addControl(drawControl);

					// Handle map events
					map.on('draw:created', (async (event: { layer: Rectangle }) => {
						console.log('Draw Created');
						const layer = event.layer;
						if (drawnItems) {
							drawnItems.clearLayers();
							drawnItems.addLayer(layer);
						}

						const bounds = layer.getBounds();
						const latMin = bounds.getSouthWest().lat;
						const lonMin = bounds.getSouthWest().lng;
						const latMax = bounds.getNorthEast().lat;
						const lonMax = bounds.getNorthEast().lng;

						// Update store with selected area
						mapState.selectedArea = { latMin, lonMin, latMax, lonMax };

						await gerarQuadrantesNaArea(latMin, lonMin, latMax, lonMax);
					}) as LeafletEventHandlerFn);
				}
			}
		};

		createMap();

		return () => {
			if (map) map.remove();
		};
	});

	async function gerarQuadrantesNaArea(
		latMin: number,
		lonMin: number,
		latMax: number,
		lonMax: number
	) {
		if (!map || !L) return;

		// Set processing state
		mapState.isProcessing = true;

		// Clear previous quadrants
		mapState.quadrants = [];

		const stepsLat = Math.ceil((latMax - latMin) / SQUARE_SIZE);
		const stepsLon = Math.ceil((lonMax - lonMin) / SQUARE_SIZE);
		const BATCH_SIZE = 4; // Process quadrants one at a time to avoid overwhelming the APIs

		const newQuadrants: QuadrantData[] = [];

		for (let i = 0; i < stepsLat; i++) {
			for (let j = 0; j < stepsLon; j += BATCH_SIZE) {
				const batchPromises = [];

				// Create a batch of promises for the current row
				for (let k = 0; k < BATCH_SIZE && j + k < stepsLon; k++) {
					const lat = latMin + i * SQUARE_SIZE;
					const lon = lonMin + (j + k) * SQUARE_SIZE;

					batchPromises.push(
						(async () => {
							const recommendedPlantForArea = await getRecommendedPlant({
								latMin,
								lonMin,
								latMax,
								lonMax
							});

							if (recommendedPlantForArea) {
								// Create quadrant data for store
								const quadrantData: QuadrantData = {
									lat,
									lon,
									plantRecommendation: recommendedPlantForArea.prediction,
									analyzedAreaData: recommendedPlantForArea.features_used
								};

								newQuadrants.push(quadrantData);

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

								return {
									bounds: [
										[lat, lon],
										[lat + SQUARE_SIZE, lon + SQUARE_SIZE]
									] as LatLngBoundsExpression,
									color: '#FF0000',
									popup: bodyWrapper
								};
							}
							return null;
						})()
					);
				}

				// Wait for all promises in the batch to resolve
				const results = await Promise.all(batchPromises);

				// Add valid results to the map
				results.forEach((result) => {
					if (result && map && L) {
						L.rectangle(result.bounds, {
							color: result.color,
							weight: 1,
							fillOpacity: 0.6
						})
							.bindPopup(result.popup)
							.addTo(map);
					}
				});

				// Update the store with current quadrants
				mapState.quadrants = newQuadrants;
			}
		}

		// Set lastAnalyzedArea with timestamp
		mapState.lastAnalyzedArea = {
			latMin,
			lonMin,
			latMax,
			lonMax,
			timestamp: Date.now()
		};

		// Set processing state to false
		mapState.isProcessing = false;
	}
</script>

<div bind:this={mapContainer} class="map"></div>

<style>
	.map {
		width: 100%;
		height: 100vh;
	}
</style>
