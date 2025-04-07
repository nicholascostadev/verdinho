<script lang="ts">
	import type {
		Map,
		FeatureGroup,
		Rectangle,
		LatLngBoundsExpression,
		LeafletEventHandlerFn
	} from 'leaflet';
	import { mapState, type QuadrantData } from '$lib/stores/mapStore.svelte';

	let mapContainer: HTMLElement | null = $state(null);
	let map: Map | null = $state(null);
	let drawnItems: FeatureGroup | null = $state(null);
	// We need to use any because of how we dynamically import Leaflet
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	let L: any;

	const OWM_API_KEY = 'ed5dbe9896c14fb2526e2c777a124718';
	const SQUARE_SIZE = $state(0.005);

	const popupClasses = (N: number) => ({
		header: `!bg-[${colorByReforestationNeed(N)}] !py-2 !px-3 !rounded-t-md !-mx-3 !-mt-2 !mb-3 !font-bold !text-center`,
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
				L.GeometryUtil.readableArea = function (
					area: number,
					isMetric: boolean,
					precision?: number
				) {
					// This variable is needed by other parts of the leaflet-draw code
					const type = isMetric ? 'metric' : 'imperial';

					// Use the type in a console log to prevent "unused variable" warning
					// This is important as other parts of the code rely on this variable existing
					if (window.console && window.console.debug) {
						window.console.debug(`Area displayed in ${type} units`);
					}

					if (isMetric) {
						if (area >= 10000) {
							return L.GeometryUtil.formattedNumber(area * 0.0001, precision) + ' ha';
						} else {
							return L.GeometryUtil.formattedNumber(area, precision) + ' m²';
						}
					} else {
						const acres = area * 0.00024711;
						if (acres >= 1) {
							return L.GeometryUtil.formattedNumber(acres, precision) + ' acres';
						} else {
							return L.GeometryUtil.formattedNumber(area, precision) + ' ft²';
						}
					}
				};
			}

			if (L.drawLocal && L.drawLocal.draw && L.drawLocal.draw.handlers) {
				// Override the rectangle handler with complete configuration
				L.drawLocal.draw.handlers.rectangle = {
					tooltip: {
						start: 'Clique e arraste para desenhar uma área.'
					},
					radius: 'Raio'
				};

				// Portuguese translation for Leaflet Draw
				L.drawLocal.draw.toolbar.buttons.rectangle = 'Desenhar um retângulo';
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

	async function fetchNDVI(lat: number, lon: number) {
		try {
			const res = await fetch('http://localhost:5000/ndvi-real', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ lat, lon })
			});
			const data = await res.json();
			return data.ndvi ?? -0.1;
		} catch (error) {
			console.error('Erro NDVI:', error);
			return -0.1;
		}
	}

	type WeatherData = {
		weather: {
			main: {
				temp: number;
				humidity: number;
				pressure: number;
			};
		};
		airQuality: {
			list: [
				{
					main: { aqi: number };
					components: { co: number };
				}
			];
		};
	};

	async function fetchWeatherAndAirData(lat: number, lon: number): Promise<WeatherData | null> {
		const weatherURL = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${OWM_API_KEY}&units=metric&lang=pt_br`;
		const airURL = `https://api.openweathermap.org/data/2.5/air_pollution?lat=${lat}&lon=${lon}&appid=${OWM_API_KEY}`;
		try {
			const weatherRes = await fetch(weatherURL);
			const airRes = await fetch(airURL);
			return {
				weather: await weatherRes.json(),
				airQuality: await airRes.json()
			};
		} catch (error) {
			console.error('Erro clima/ar:', error);
			return null;
		}
	}

	async function consultarMelhorPlanta(data: WeatherData, lat: number, lon: number) {
		try {
			const res = await fetch('http://localhost:5000/melhor-planta', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					temperatura: data.weather.main.temp,
					umidade: data.weather.main.humidity,
					pressao: data.weather.main.pressure,
					co: data.airQuality.list[0].components.co,
					aqi: data.airQuality.list[0].main.aqi,
					lat,
					lon
				})
			});
			return await res.json();
		} catch (error) {
			console.error('Erro consulta planta:', error);
			return { planta_recomendada: 'Erro IA', bioma: '-', regiao: '-' };
		}
	}

	function calculateReforestationIndex(ndvi: number, aqi: number) {
		if (!mapState.enableNdvi) {
			// If NDVI is disabled, only consider air quality
			return Math.min(aqi / 5, 1);
		}

		const ndviNorm = 1 - (ndvi + 1) / 2;
		const aqiNorm = Math.min(aqi / 5, 1);
		return 0.5 * ndviNorm + 0.5 * aqiNorm;
	}

	function getReforestationNeedLevel(N: number) {
		if (N <= 0.2) return 'Sem Necessidade';
		if (N <= 0.4) return 'Baixa Necessidade';
		if (N <= 0.6) return 'Necessidade Moderada';
		if (N <= 0.8) return 'Necessidade Alta';
		return 'Necessidade Extrema';
	}

	function colorByReforestationNeed(N: number) {
		if (N <= 0.2) return '#008000';
		if (N <= 0.4) return '#9ACD32';
		if (N <= 0.6) return '#FFD700';
		if (N <= 0.8) return '#FFA500';
		return '#FF0000';
	}

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
		const BATCH_SIZE = 1; // Process quadrants one at a time to avoid overwhelming the APIs

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
							const [ndvi, data] = await Promise.all([
								mapState.enableNdvi ? fetchNDVI(lat, lon) : Promise.resolve(0),
								fetchWeatherAndAirData(lat, lon)
							]);

							if (data) {
								const aqi = data.airQuality.list[0].main.aqi;
								// Use a default NDVI value of 0 if NDVI is disabled
								const N = calculateReforestationIndex(ndvi, aqi);
								const ia = await consultarMelhorPlanta(data, lat, lon);

								// Create quadrant data for store
								const quadrantData: QuadrantData = {
									lat,
									lon,
									ndvi,
									aqi,
									refIndex: N,
									needLevel: getReforestationNeedLevel(N),
									plantRecommendation: ia
								};

								newQuadrants.push(quadrantData);

								const popup = popupClasses(N);

								return {
									bounds: [
										[lat, lon],
										[lat + SQUARE_SIZE, lon + SQUARE_SIZE]
									] as LatLngBoundsExpression,
									color: colorByReforestationNeed(N),
									popup: `
									<div class="${popup.header}">
										${getReforestationNeedLevel(N)}
									</div>
									<div class="${popup.body}">
										<div class="${popup.row}">
											<span class="${popup.icon}">🌿</span>
											<strong class="${popup.label}">Planta:</strong> <span class="${popup.value}">${ia.planta_recomendada}</span>
										</div>
										${
											mapState.enableNdvi
												? `
										<div class="${popup.row}">
											<span class="${popup.icon}">🛰️</span>
											<strong class="${popup.label}">NDVI:</strong> <span class="${popup.value}">${ndvi.toFixed(2)}</span>
										</div>
										`
												: ''
										}
										<div class="${popup.row}">
											<span class="${popup.icon}">💨</span>
											<strong class="${popup.label}">AQI:</strong> <span class="${popup.value}">${aqi}</span>
										</div>
										<div class="${popup.row}">
											<span class="${popup.icon}">🌎</span>
											<strong class="${popup.label}">Bioma:</strong> <span class="${popup.value}">${ia.bioma}</span>
										</div>
										<div class="${popup.row}">
											<span class="${popup.icon}">🗺️</span>
											<strong class="${popup.label}">Região:</strong> <span class="${popup.value}">${ia.regiao}</span>
										</div>
									</div>
                `
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
