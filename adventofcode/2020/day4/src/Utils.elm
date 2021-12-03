module Utils exposing (decimal, indexes, element, letters)

import Array
import Binary
import Parser exposing (Parser, succeed, (|.), chompWhile, getChompedString)


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


slice : Int -> Int -> List a -> List a
slice start end list =
    List.take (List.length list - end) list
        |> List.drop start


-- Parser


letters : Parser String
letters =
    succeed ()
        |. chompWhile Char.isAlpha
        |> getChompedString

