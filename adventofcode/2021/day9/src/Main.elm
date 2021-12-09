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
               , cols 50
               , class "bg-dark text-white-50 border-1 border-secondary p-2"
               ] []
    , div [] [ a [ href (linkToInput 2021 9)
             , target "_blank"
             , class "text-white-50"
             ] [ text "Link to puzzle's input" ] ]
    , div [] [ text ( "Input: " ++ viewModel model ) ]
    , div [] [ text ( "Solution 1: " ++ viewSolution ( solution1 model.input ) ) ]
    , div [] [ text ( "Test 1: " ++ testSolution 15 ( solution1 (parseInput defaultContent) ) ) ]
    , div [] [ text ( "Solution 2: " ++ viewSolution ( solution2 model.input ) ) ]
    , div [] [ text ( "Test 2: " ++ testSolution 1134 ( solution2 (parseInput defaultContent) ) ) ]
    ]


viewModel : Model -> String
viewModel model =
    (++) "number of points = "
        <| String.fromInt (List.length (Dict.toList model.input))


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


type alias Input = HeightMap


type alias HeightMap = Dict.Dict (Int, Int) Int



defaultContent =
    """2199943210
3987894921
9856789892
8767896789
9899965678"""


parseInput : String -> Input
parseInput string =
    let
        toInt char =
            Maybe.withDefault 0 (String.toInt (String.fromChar char))
        iFoldl =
            List.Extra.indexedFoldl
    in
    String.trim string
        |> String.lines
        |> List.map String.toList
        |> iFoldl (\y row heightMap -> iFoldl (\x value map -> Dict.insert (x, y) (toInt value) map) heightMap row) Dict.empty


solution1 : Input -> Maybe Int
solution1 heightmap =
    let
        isLowPoint ((x, y), height) =
            let
                up =
                    Dict.get (x - 1, y) heightmap
                down =
                    Dict.get (x + 1, y) heightmap
                left =
                    Dict.get (x, y - 1) heightmap
                right =
                    Dict.get (x, y + 1) heightmap
                neighbors =
                    [up, down, left, right]
                checkNeighbor neighbor acc =
                    case neighbor of
                        Nothing ->
                            acc && True
                        Just val ->
                            acc && val > height
            in
            List.foldl checkNeighbor True neighbors
        riskLevel (_, height) sum =
            sum + height + 1
    in
    Dict.toList heightmap
        |> List.filter isLowPoint
        |> List.foldl riskLevel 0
        |> Just


solution2 : Input -> Maybe Int
solution2 heightmap =
    solution1 heightmap

