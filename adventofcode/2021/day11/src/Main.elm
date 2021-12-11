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
    , div [] [ a [ href (linkToInput 2021 11)
             , target "_blank"
             , class "text-white-50"
             ] [ text "Link to puzzle's input" ] ]
    , div [] [ text ( "Input: " ++ viewModel model.input ) ]
    , div [] [ text ( "Solution 1: " ++ viewSolution ( solution1 model.input ) ) ]
    , div [] [ text ( "Test 1: " ++ testSolution 1656 ( solution1 (parseInput defaultContent) ) ) ]
    , div [] [ text ( "Solution 2: " ++ viewSolution ( solution2 model.input ) ) ]
    , div [] [ text ( "Test 2: " ++ testSolution 195 ( solution2 (parseInput defaultContent) ) ) ]
    ]


viewModel : Input -> String
viewModel input =
    (++) "number of octopuses = "
        <| String.fromInt (List.length (Dict.toList input))


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


type alias Input = EnergyChart


type alias EnergyChart = Dict.Dict (Int, Int) (Bool, Int)



defaultContent =
    """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


parseInput : String -> Input
parseInput string =
    Utils.stringToMatrix string
        |> Dict.toList
        |> List.foldl (\(key, value) -> Dict.insert key (False, value)) Dict.empty


solution1 : Input -> Maybe Int
solution1 input =
    let
        after100Steps =
            List.range 0 99
                |> List.foldl performStep (0, input)
        performStep _ (totalFlashes, chart) =
            case step chart of
                (flashCount, outputChart) ->
                    (totalFlashes + flashCount, Dict.map (\_ (_, energy) -> (False, energy)) outputChart)
    in
    case after100Steps of
        (flashes, _) ->
            Just flashes


solution2 : Input -> Maybe Int
solution2 input =
    findStepAllFlashing 1 input
        |> Just


findStepAllFlashing : Int -> EnergyChart -> Int
findStepAllFlashing idx chart =
    case step chart of
        (_, outputChart) ->
            if isAllFlashing outputChart then
                idx
            else
                findStepAllFlashing (idx + 1) (Dict.map (\_ (_, energy) -> (False, energy)) outputChart)


isAllFlashing : EnergyChart -> Bool
isAllFlashing chart =
    let
        points =
            Dict.toList chart
        numFlashing =
            List.foldl (\(_, (excited, _)) acc -> acc + if excited then 1 else 0) 0 points
   in
   numFlashing == List.length points


step : EnergyChart -> (Int, EnergyChart)
step chart =
    let
        plusOneChart =
            Dict.map (\_ (excited, value) -> (excited, value + 1)) chart
    in
    exciteChain 0 plusOneChart


exciteChain : Int -> EnergyChart -> (Int, EnergyChart)
exciteChain flashCount chart =
    let
        isPointAboutToFlash (excited, energy) =
            energy > 9 && excited == False
        aboutToFlash matrix =
            Dict.foldl (\coord point acc -> if isPointAboutToFlash point then coord :: acc else acc) [] matrix
    in
    case aboutToFlash chart of
        [] ->
            (flashCount, chart)
        xs ->
            List.foldl flashPoint chart xs
                |> exciteChain (flashCount + List.length xs)


flashPoint : (Int, Int) -> EnergyChart -> EnergyChart
flashPoint (x, y) chart =
    let
        potentialPoints =
            [ (x + 1, y + 1)
            , (x, y + 1)
            , (x - 1, y + 1)
            , (x - 1, y)
            , (x - 1, y - 1)
            , (x, y - 1)
            , (x + 1, y - 1)
            , (x + 1, y)
            ]
        isSurroundingPoint point =
            case Dict.get point chart of
                Nothing ->
                    False
                Just _ ->
                    True
        surroundingPoints =
            List.filter isSurroundingPoint potentialPoints
        updatePoint val =
            case val of
                Nothing ->
                    Nothing
                Just (excited, value) ->
                    if excited then
                        Just (excited, value)
                    else
                        Just (excited, value + 1)
    in
    List.foldl (\point acc -> Dict.update point updatePoint acc) (Dict.insert (x, y) (True, 0) chart) surroundingPoints


