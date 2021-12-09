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


type alias HeightMap = Dict.Dict Coordinates Int


type alias HeightPoint = (Coordinates, Int)


type alias Coordinates = (Int, Int)


type alias Basin = HeightMap



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
        riskLevel (_, height) sum =
            sum + height + 1
    in
    getLowPoints heightmap
        |> List.foldl riskLevel 0
        |> Just


solution2 : Input -> Maybe Int
solution2 heightmap =
    let
        lowPoints =
            getLowPoints heightmap
        basins =
            List.map (\(point, height) -> searchBasin heightmap (Dict.insert point height Dict.empty) (List.singleton point)) lowPoints
        basinSizes =
            List.map (\basin -> List.length (Dict.toList basin)) basins
    in
    basinSizes
        |> List.sort
        |> List.reverse
        |> List.take 3
        |> List.product
        |> Just


getLowPoints : HeightMap -> List HeightPoint
getLowPoints heightmap =
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
    in
    Dict.toList heightmap
        |> List.filter isLowPoint


searchBasin : HeightMap -> Basin -> List Coordinates -> Basin
searchBasin heightmap basin nextCoordinates =
    case nextCoordinates of
        [] ->
            basin
        _ ->
            let
                step (x, y) (nextBasin, nextCoords) =
                    let
                        getNeighbor neighborCoord =
                            case Dict.get neighborCoord heightmap of
                                Nothing ->
                                    Nothing
                                Just neighborHeight ->
                                    let
                                        height =
                                            Maybe.withDefault 0 (Dict.get (x, y) heightmap)
                                    in
                                    if neighborHeight > height && neighborHeight < 9 then
                                        case Dict.get neighborCoord nextBasin of
                                            Nothing ->
                                                Just (neighborCoord, neighborHeight)
                                            Just _ ->
                                                Nothing
                                    else
                                        Nothing
                        up =
                            getNeighbor (x - 1, y)
                        down =
                            getNeighbor (x + 1, y)
                        left =
                            getNeighbor (x, y - 1)
                        right =
                            getNeighbor (x, y + 1)
                        neighbors =
                            [up, down, left, right]
                        validNeighbors =
                            List.filterMap identity neighbors
                        updateBasin neighbor updatedBasin =
                            case neighbor of
                                (c, h) ->
                                    Dict.insert c h updatedBasin
                    in
                    ( List.foldl updateBasin nextBasin validNeighbors
                    , List.append (List.map (\(vnCoords, _) -> vnCoords) validNeighbors) nextCoords
                    )
            in
            case List.foldl step (basin, []) nextCoordinates of
                (b, nc) ->
                    searchBasin heightmap b nc

