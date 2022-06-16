function solution(H) {
    let counter = 0;
    const missed = [];
    missed.push(H);
    while (missed.length > 0) {
        counter += putBlocks(missed.pop(), missed);
    }
    return counter;
}

function putBlocks(H, missed) {
    let counter = 1;
    let newMissed = [];
    let height = H[0];
    for (let i = 1; i < H.length; i++) {
        if (H[i] === height) {
            if (newMissed.length) {
                missed.push(newMissed);
                newMissed = [];
            } 
        } else if (H[i] > height) {
            newMissed.push(H[i] - height);
        } else if (H[i] < height) {
            counter++;
            height = H[i];
            if (newMissed.length) {
                missed.push(newMissed);
                newMissed = [];
            }
        }
    }
    if (newMissed.length) {
        missed.push(newMissed);
    }
    return counter;
}

