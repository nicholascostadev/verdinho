import type { QuadrantData } from './mapStore.svelte';

class QuadrantModalStore {
	quadrant: QuadrantData | null = $state(null);
	isOpen = $state(false);

	updateQuadrant(quadrant: QuadrantData) {
		this.quadrant = quadrant;
	}

	openModal() {
		this.isOpen = true;
	}
}

export const quadrantModalStore = new QuadrantModalStore();
