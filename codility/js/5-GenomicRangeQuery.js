function solution(S, P, Q) {
    let A = [],
        C = [],
        G = [];
    for (let i = 0; i < S.length; i++) {
        switch (S[i]) {
            case 'A':
                A.push(i);
                break;
            case 'C':
                C.push(i);
                break;
            case 'G':
                G.push(i);
                break;
        }
    }
    
    const result = new Array(P.length);
    for (let i = 0; i < P.length; i++) {
        if (checkForNucleotid(A, P[i], Q[i])) {
            result[i] = 1;
            continue;
        }
        if (checkForNucleotid(C, P[i], Q[i])) {
            result[i] = 2;
            continue;
        }
        if (checkForNucleotid(G, P[i], Q[i])) {
            result[i] = 3;
            continue;
        }
        result[i] = 4;
    }
    return result;
}

function checkForNucleotid(nucleotid, p, q) {
    for (let i = 0; i < nucleotid.length; i++) {
        if (p <= nucleotid[i] && q >= nucleotid[i]) {
            return true;
        }
    }
    return false;
}

