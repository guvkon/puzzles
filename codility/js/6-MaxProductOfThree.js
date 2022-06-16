function solution(A) {
    A.sort((a, b) => a - b);
    const edges = [];
    for (let i = 0; i < 3; i++) {
        edges.push(A[i]);
    }
    for (let i = Math.max(3, A.length - 3); i < A.length; i++) {
        edges.push(A[i]);
    }
    let maxProduct = false;
    for (let i = 0; i < edges.length; i++) {
        for (let j = 0; j !== i && j < edges.length; j++) {
            for (let k = 0; k < edges.length && k !== j; k++) {
                const product = edges[i] * edges[j] * edges[k];
                if (maxProduct === false || maxProduct < product) {
                    maxProduct = product;
                }
            }
        }
    }
    return maxProduct;
}

