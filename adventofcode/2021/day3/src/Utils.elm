module Utils exposing (decimal, indexes, element)

import Array
import Binary


-- Binary


decimal : List Int -> Int
decimal bits =
    Binary.fromIntegers bits
        |> Binary.toDecimal


-- List


indexes : List a -> List Int
indexes list =
    List.range 0 (List.length list - 1)


element : Int -> List a -> Maybe a
element index list =
    Array.fromList list
        |> Array.get index


