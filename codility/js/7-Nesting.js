function solution(S) {
    const stack = [];
    for (let i = 0; i < S.length; i++) {
        switch (S[i]) {
            case '(':
                stack.push(S[i]);
                break;
            case ')':
                const last = stack.pop();
                if (last !== '(') {
                    return 0;
                }
                break;
        }
    }
    return stack.length === 0 ? 1 : 0;
}

