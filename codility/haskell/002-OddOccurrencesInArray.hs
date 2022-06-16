import Data.List

solution :: (Integral a) => [a] -> a
solution xs = head $ foldl1 (\acc xs -> if odd (length xs) then xs else acc) (group $ sort xs)
