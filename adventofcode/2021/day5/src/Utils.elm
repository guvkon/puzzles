module Utils exposing (decimal, parseStringIntoBlocks, indexes, element, field, rotateMatrix, counter, letters, stringEntry, exists, count)

import Array
import Binary
import Parser exposing ((|.), Parser, chompIf, chompWhile, getChompedString, succeed)


-- Binary


decimal : List Int -> Int
decimal bits =
    Binary.fromIntegers bits
        |> Binary.toDecimal


-- String


parseStringIntoBlocks : String -> List String
parseStringIntoBlocks str =
    String.lines str
        |> groupStrings [] []
        |> List.filter (not << String.isEmpty)
        |> List.reverse


groupStrings : List String -> List String -> List String -> List String
groupStrings temp result rawList =
    let
        append y ys =
            (String.join "\n" y) :: ys
    in
    case rawList of
        x :: xs ->
            if x == "" then
                groupStrings [] (append temp result) xs
            else
                groupStrings (x :: temp) result xs
        [] -> append temp result


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


rotateMatrix : List (List a) -> List (List a)
rotateMatrix matrix =
    let
        step =
            \index ->
                List.filterMap (element index) matrix
    in
    case matrix of
        x :: _ ->
            indexes x
                |> List.map step
        [] -> []


counter : (a -> Bool) -> a -> Int -> Int
counter compare val acc =
    acc + if compare val then 1 else 0


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

