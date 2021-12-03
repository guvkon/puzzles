module Utils exposing (decimal, indexes, element, field, letters, stringEntry, exists, count)

import Array
import Binary
import Parser exposing ((|.), Parser, chompIf, chompWhile, getChompedString, succeed)


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


field : (a -> String) -> (a -> b) -> String -> List a -> Maybe b
field getKey getValue name record =
    case record of
        [] ->
            Nothing
        x :: xs ->
            if getKey x == name then
                Just (getValue x)
            else
                field getKey getValue name xs


-- Bool


exists : Maybe a -> Bool
exists x =
    case x of
        Just _ -> True
        Nothing -> False


count : Bool -> Int
count x =
    if x then
        1
    else
        0


-- Parser


letters : Parser String
letters =
    stringEntry Char.isAlpha


stringEntry : (Char -> Bool) -> Parser String
stringEntry check =
    succeed ()
        |. chompIf check
        |. chompWhile check
        |> getChompedString

