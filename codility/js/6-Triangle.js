function solution(A) {
    A.sort((a, b) => a - b);

    let result = 0;
    for (let i = 0; i < A.length - 2; i++) {
        if (isTriangle(A[i], A[i+1], A[i+2])) {
            result = 1;
            break;
        }
    }
    return result;
}

const isTriangle = (a, b, c) => {
    return a + b > c && c + a > b && b + c > a;
}
