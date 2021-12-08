module Main exposing (..)

import Basics
import Browser
import Dict
import Html exposing (Html, Attribute, div, a, textarea, text)
import Html.Attributes exposing (class, cols, href, placeholder, rows, target, value)
import Html.Events exposing (onInput)
import Matrix
import Parser exposing ((|.), (|=), Parser, int, spaces, succeed, symbol)
import Utils
import List.Extra


-- MAIN


main =
  Browser.sandbox { init = init, update = update, view = view }



-- MODEL


type alias Model =
  { input : Input
  , content : String
  }


init : Model
init =
  { input = parseInput defaultContent
  , content = defaultContent
  }



-- UPDATE


type Msg
  = Change String


update : Msg -> Model -> Model
update msg model =
  case msg of
    Change newContent ->
      { model | content = newContent, input = parseInput newContent }



-- VIEW


view : Model -> Html Msg
view model =
  div []
    [ textarea [ placeholder "Input"
               , value model.content
               , onInput Change
               , rows 20
               , cols 90
               , class "bg-dark text-white-50 border-1 border-secondary p-2"
               ] []
    , div [] [ a [ href (linkToInput 2021 8)
             , target "_blank"
             , class "text-white-50"
             ] [ text "Link to puzzle's input" ] ]
    , div [] [ text ( "Input: " ++ viewModel model ) ]
    , div [] [ text ( "Solution 1: " ++ viewSolution ( solution1 model.input ) ) ]
    , div [] [ text ( "Test 1: " ++ testSolution 26 ( solution1 (parseInput defaultContent) ) ) ]
    , div [] [ text ( "Solution 2: " ++ viewSolution ( solution2 model.input ) ) ]
    , div [] [ text ( "Test 2: " ++ testSolution 61229 ( solution2 (parseInput defaultContent) ) ) ]
    ]


viewModel : Model -> String
viewModel model =
    (++) "lines to decode = "
        <| String.fromInt (List.length model.input)


viewSolution : Maybe Int -> String
viewSolution solution =
    case solution of
        Just val ->
            String.fromInt val
        Nothing ->
            "NaN"


testSolution : Int -> Maybe Int -> String
testSolution target result =
    case result of
        Nothing ->
            "Error"
        Just val ->
            if val == target then
                "Passing"
            else
                "Error"


linkToInput : Int -> Int -> String
linkToInput year day =
    "https://adventofcode.com/"
        ++ (String.fromInt year)
        ++ "/day/"
        ++ (String.fromInt day)
        ++ "/input"



-- LOGIC


type alias Input = List (List String, List String)


type alias Cypher = Dict.Dict Char Char


type alias Solution = Dict.Dict String String


type alias Light = List Char


defaultContent =
    """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


parseInput : String -> Input
parseInput string =
    let
        parseSection str =
            String.words str
        parseLine str =
            String.split " | " str
                |> List.map parseSection
        convertToTuple strings =
            ( Maybe.withDefault [] (Utils.element 0 strings)
            , Maybe.withDefault [] (Utils.element 1 strings)
            )
    in
    String.trim string
        |> String.lines
            |> List.map parseLine
                |> List.map convertToTuple


solution1 : Input -> Maybe Int
solution1 input =
    let
        match : String -> Bool
        match str =
            case String.length str of
                2 -> True
                4 -> True
                3 -> True
                7 -> True
                _ -> False
        count : (List String, List String) -> Int
        count pair =
            case pair of
                (_, right) ->
                    right
                        |> List.foldl (Utils.counter match) 0
    in
    input
        |> List.foldl (\pair sum -> sum + count pair) 0
        |> Just


solution2 : Input -> Maybe Int
solution2 input =
    let
        decodeLine : (List String, List String) -> String
        decodeLine pair =
            case pair of
                (left, right) ->
                    let
                        cypher =
                            compileCypher left
                        decoder =
                            decodeLight cypher
                    in
                    right
                        |> List.filterMap decoder
                        |> List.map String.fromInt
                        |> String.join ""
    in
    input
        |> List.map decodeLine
        |> List.filterMap String.toInt
        |> List.sum
        |> Just


compileCypher : List String -> Cypher
compileCypher strings =
    let
        len =
            String.length
        toStr =
            String.fromChar
        has =
            String.contains
        hasChar char =
            has (toStr char)
        notHasChar char =
            not << (hasChar char)
        lenN number default =
            List.foldl (\str acc -> if len str == number then str else acc ) default strings
        cf =
            lenN 2 "cf"
        acf =
            lenN 3 "acf"
        a =
            List.foldl (\char acc -> if notHasChar char cf then char else acc) 'a' (String.toList acf)
        bdcf =
            lenN 4 "bdcf"
        bd =
            List.filter (\char -> notHasChar char cf) (String.toList bdcf)
                |> String.fromList
        all =
            "abcdefg"
        abdcf =
            (toStr a) ++ bdcf
        eg =
            List.filter (\char -> notHasChar char abdcf) (String.toList all)
                |> String.fromList
        len6 =
            List.filter (\str -> len str == 6) strings
        common strs =
            List.foldl (\str remaining -> List.filter (\char -> hasChar char str) remaining) (String.toList all) strs
                |> String.fromList
        abfg =
            common len6
        bfg =
            List.filter (\chr -> chr /= a) (String.toList abfg)
                |> String.fromList
        len5 =
            List.filter (\str -> len str == 5) strings
        adg =
            common len5
        dg =
            List.filter (\chr -> chr /= a) (String.toList adg)
                |> String.fromList
        d =
            List.foldl (\char acc -> if hasChar char bd then char else acc) 'd' (String.toList dg)
        b =
            List.foldl (\char acc -> if char /= d then char else acc) 'b' (String.toList bd)
        g =
            List.foldl (\char acc -> if char /= d then char else acc) 'g' (String.toList dg)
        e =
            List.foldl (\char acc -> if char /= g then char else acc) 'e' (String.toList eg)
        f =
            List.foldl (\char acc -> if char /= b && char /= g then char else acc) 'f' (String.toList bfg)
        allExceptC =
            [a, b, d, e, f, g]
                |> String.fromList
        c =
            List.foldl (\char acc -> if notHasChar char allExceptC then char else acc) 'c' (String.toList all)
    in
    Dict.empty
        |> Dict.insert a 'a'
        |> Dict.insert b 'b'
        |> Dict.insert c 'c'
        |> Dict.insert d 'd'
        |> Dict.insert e 'e'
        |> Dict.insert f 'f'
        |> Dict.insert g 'g'


decodeLight : Cypher -> String -> Maybe Int
decodeLight cypher light =
    String.toList light
        |> List.filterMap (\char -> Dict.get char cypher)
        |> lightToNumber


lightToNumber : Light -> Maybe Int
lightToNumber light =
    case String.fromList (List.sort light) of
        "cf" ->
            Just 1
        "acf" ->
            Just 7
        "bcdf" ->
            Just 4
        "acdeg" ->
            Just 2
        "acdfg" ->
            Just 3
        "abdfg" ->
            Just 5
        "abcefg" ->
            Just 0
        "abdefg" ->
            Just 6
        "abcdfg" ->
            Just 9
        "abcdefg" ->
            Just 8
        _ ->
            Nothing

