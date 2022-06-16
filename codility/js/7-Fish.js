function solution(A, B) {
    const fishes = [];
    for (let i = 0; i < B.length; i++) {
        const fish = { size: A[i], direction: B[i] };
        while (interact(fishes, fish));
    }
    return fishes.length;
}

const DOWNSTREAM_DIRECTION = 1;
const UPSTREAM_DIRECTION = 0;

const interact = (fishes, fish) => {
    if (fishes.length === 0) {
        fishes.push(fish);
    } else {
        const lastFish = fishes[fishes.length - 1];
        if (lastFish.direction === DOWNSTREAM_DIRECTION && fish.direction === UPSTREAM_DIRECTION) {
            if (lastFish.size < fish.size) {
                fishes.pop();
                return true;
            }
        } else {
            fishes.push(fish);
        }
    }
    return false;
}

