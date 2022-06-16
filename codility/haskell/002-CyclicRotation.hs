solution :: Int -> [a] -> [a]
solution 0 x = x
solution _ [] = []
solution n x = solution (n - 1) $ [last x] ++ init x
