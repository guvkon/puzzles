function solution(S) {
    const A = [];
    const map = {
        ')': '(',
        ']': '[',
        '}': '{'
    };
    for (let i = 0; i < S.length; i++) {
        switch (S[i]) {
            case '(':
            case '[':
            case '{':
                A.push(S[i]);
                break;
            case ')':
            case ']':
            case '}':
                const last = A.pop();
                if (!last || map[S[i]] !== last) {
                    return 0;
                }
                break;
        }
    }
    return A.length === 0 ? 1 : 0;
}
