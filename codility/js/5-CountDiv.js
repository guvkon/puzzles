function solution(A, B, K) {
    const ka = Math.floor(A / K);
    const kb = Math.floor(B / K);
    let result = kb - ka;
    if (A % K === 0) {
        result++;
    }
    return result;
}
