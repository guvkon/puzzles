function solution(A) {
    if (A.length === 2) {
        return Math.abs(A[0] - A[1]);
    }
    
    let sumRight = 0,
        sumLeft = A[0];
    for (let i = 1; i < A.length; i++) {
        sumRight += A[i];
    }
    let min = Math.abs(sumLeft - sumRight);
    for (let i = 1; i < A.length - 1; i++) {
        sumRight -= A[i];
        sumLeft += A[i];
        const diff = Math.abs(sumRight - sumLeft);
        if (diff < min) {
            min = diff;
        }
    }
    return min;
}
