function solution(A) {
    const found = {};
    let distinctCount = 0;
    for (let i = 0; i < A.length; i++) {
        if (found[A[i]] === undefined) {
            distinctCount++;
            found[A[i]] = true;
        }
    }
    return distinctCount;
}
