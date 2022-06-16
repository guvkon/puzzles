solution :: (Integral a) => a -> a
solution = snd . foldl binarygap (0, 0) . binary

binary :: (Integral a) => a -> [a]
binary 0 = [0]
binary 1 = [1]
binary x = binary (x `div` 2) ++ [x `mod` 2]

binarygap :: (Integral a) => (a, a) -> a -> (a, a)
binarygap (curgap, maxgap) x
    | x == 0          = (curgap + 1, maxgap)
    | curgap > maxgap = (0, curgap)
    | otherwise       = (0, maxgap)

