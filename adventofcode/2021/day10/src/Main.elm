module Main exposing (..)

import Basics
import Browser
import Dict
import Html exposing (Html, Attribute, div, a, textarea, text)
import Html.Attributes exposing (class, cols, href, placeholder, rows, target, value)
import Html.Events exposing (onInput)
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
               , cols 60
               , class "bg-dark text-white-50 border-1 border-secondary p-2"
               ] []
    , div [] [ a [ href (linkToInput 2021 10)
             , target "_blank"
             , class "text-white-50"
             ] [ text "Link to puzzle's input" ] ]
    , div [] [ text ( "Input: " ++ viewModel model.input ) ]
    , div [] [ text ( "Solution 1: " ++ viewSolution ( solution1 model.input ) ) ]
    , div [] [ text ( "Test 1: " ++ testSolution 26397 ( solution1 (parseInput defaultContent) ) ) ]
    , div [] [ text ( "Solution 2: " ++ viewSolution ( solution2 model.input ) ) ]
    , div [] [ text ( "Test 2: " ++ testSolution 288957 ( solution2 (parseInput defaultContent) ) ) ]
    ]


viewModel : Input -> String
viewModel input =
    (++) "number of lines = "
        <| String.fromInt (List.length input)


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


type alias Input = List String


type alias TokenSearch = { openBrackets : List Char, illegalToken : Maybe Char }



defaultContent =
    """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


parseInput : String -> Input
parseInput string =
    string
        |> String.trim
        |> String.lines


solution1 : Input -> Maybe Int
solution1 input =
    let
        getIllegalToken string =
            case tokenSearch string of
                { illegalToken } ->
                    illegalToken

        calculateCorruptedChunkScore char =
            case char of
                ')' -> 3
                ']' -> 57
                '}' -> 1197
                '>' -> 25137
                _ -> 0
    in
    input
        |> List.filterMap getIllegalToken
        |> List.map calculateCorruptedChunkScore
        |> List.sum
        |> Just


solution2 : Input -> Maybe Int
solution2 input =
    let
        getBracketsForIncompleteChunk string =
            case tokenSearch string of
                { openBrackets, illegalToken } ->
                    case illegalToken of
                        Nothing ->
                            case openBrackets of
                                [] ->
                                    Nothing
                                xs ->
                                    Just xs
                        Just _ ->
                            Nothing
        calculateIncompleteChunkScore brackets =
            brackets
                |> List.foldl (\char score -> 5 * score + (charToScore char)) 0
        charToScore char =
            case char of
                '(' -> 1
                '[' -> 2
                '{' -> 3
                '<' -> 4
                _ -> 0
        scores =
            input
                |> List.filterMap getBracketsForIncompleteChunk
                |> List.map calculateIncompleteChunkScore
                |> List.sort
    in
    Utils.element ((List.length scores) // 2) scores


tokenSearch : String -> TokenSearch
tokenSearch string =
    let
        closingBrackets =
            [')', '}', ']', '>']

        step char search =
            case search of
                { openBrackets, illegalToken } ->
                    case illegalToken of
                        Nothing ->
                            case openBrackets of
                                [] ->
                                    { search | openBrackets = char :: [] }
                                x :: xs ->
                                    if x == '(' && char == ')' || x == '{' && char == '}' || x == '[' && char == ']' || x == '<' && char == '>' then
                                        { search | openBrackets = xs }
                                    else if List.member char closingBrackets then
                                        { search | illegalToken = Just char }
                                    else
                                        { search | openBrackets = char :: x :: xs }
                        Just _ ->
                            search
    in
    String.toList string
        |> List.foldl step (TokenSearch [] Nothing)

