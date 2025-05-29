export type MediaResult = {
	type: string;
	format: string;
	references: string;
	created: string;
	creator: string;
	publisher: string;
	license: string;
	rightsHolder: string;
	identifier: string;
};

export type PlantGallery = {
	offset: number;
	limit: number;
	endOfRecords: boolean;
	count: number;
	results: Array<{
		key: number;
		datasetKey: string;
		publishingOrgKey: string;
		installationKey: string;
		hostingOrganizationKey: string;
		publishingCountry: string;
		protocol: string;
		lastCrawled: string;
		lastParsed: string;
		crawlId: number;
		extensions: {
			'http://rs.gbif.org/terms/1.0/Multimedia': Array<{
				'http://purl.org/dc/terms/references': string;
				'http://purl.org/dc/terms/created': string;
				'http://rs.tdwg.org/dwc/terms/catalogNumber': string;
				'http://purl.org/dc/terms/identifier': string;
				'http://purl.org/dc/terms/format': string;
				'http://purl.org/dc/terms/rightsHolder': string;
				'http://purl.org/dc/terms/creator': string;
				'http://purl.org/dc/terms/license': string;
				'http://purl.org/dc/terms/type': string;
				'http://purl.org/dc/terms/publisher': string;
			}>;
		};
		basisOfRecord: string;
		occurrenceStatus: string;
		taxonKey: number;
		kingdomKey: number;
		phylumKey: number;
		classKey: number;
		orderKey: number;
		familyKey: number;
		genusKey: number;
		speciesKey: number;
		acceptedTaxonKey: number;
		scientificName: string;
		acceptedScientificName: string;
		kingdom: string;
		phylum: string;
		order: string;
		family: string;
		genus: string;
		species: string;
		genericName: string;
		specificEpithet: string;
		taxonRank: string;
		taxonomicStatus: string;
		iucnRedListCategory: string;
		dateIdentified: string;
		decimalLatitude: number;
		decimalLongitude: number;
		continent: string;
		stateProvince: string;
		gadm: {
			level0: {
				gid: string;
				name: string;
			};
			level1: {
				gid: string;
				name: string;
			};
			level2: {
				gid: string;
				name: string;
			};
			level3?: {
				gid: string;
				name: string;
			};
		};
		year: number;
		month: number;
		day: number;
		eventDate: string;
		startDayOfYear: number;
		endDayOfYear: number;
		issues: Array<string>;
		modified: string;
		lastInterpreted: string;
		references: string;
		license: string;
		isSequenced: boolean;
		identifiers: Array<{
			identifier: string;
		}>;
		media: Array<MediaResult>;
		facts: Array<any>;
		relations: Array<any>;
		isInCluster: boolean;
		datasetName: string;
		recordedBy: string;
		identifiedBy: string;
		dnaSequenceID: Array<any>;
		geodeticDatum: string;
		class: string;
		countryCode: string;
		recordedByIDs: Array<any>;
		identifiedByIDs: Array<any>;
		gbifRegion: string;
		country: string;
		publishedByGbifRegion: string;
		rightsHolder: string;
		identifier: string;
		'http://unknown.org/nick': string;
		verbatimEventDate: string;
		collectionCode: string;
		gbifID: string;
		verbatimLocality: string;
		occurrenceID: string;
		taxonID: string;
		'http://unknown.org/captive_cultivated': string;
		catalogNumber: string;
		institutionCode: string;
		eventTime: string;
		reproductiveCondition?: string;
		identificationID: string;
		coordinateUncertaintyInMeters?: number;
		occurrenceRemarks?: string;
		identificationRemarks?: string;
	}>;
	facets: Array<any>;
};

export async function queryPlantByName(plantId: string) {
	const response = await fetch(
		`https://api.gbif.org/v1/occurrence/search?mediaType=StillImage&speciesKey=${plantId}`
	);

	const data = (await response.json()) as PlantGallery;

	return data.results.map((result) => result.media).flat();
}
