solution :: (Integral a) => a -> a -> a -> a
solution x y d = ceiling $ (fromIntegral (y - x)) / (fromIntegral d)
