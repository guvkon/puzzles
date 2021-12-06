module Main exposing (..)

import Basics as Math
import Browser
import Dict exposing (Dict)
import Html exposing (Html, Attribute, div, textarea, text)
import Html.Attributes exposing (..)
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
  { input : List Vector
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
               , cols 40
               , class "bg-secondary text-light border-1 border-dark p-2"
               ] []
    , div [] [ text ( "Input: " ++ viewModel model ) ]
    , div [] [ text ( "Solution 1: " ++ viewSolution ( solution1 model ) ) ]
    , div [] [ text ( "Solution 2: " ++ viewSolution ( solution2 model ) ) ]
    ]


viewModel : Model -> String
viewModel model =
    (++) "number of vectors = "
        <| (String.fromInt (List.length model.input))


viewSolution : Maybe Int -> String
viewSolution solution =
    case solution of
        Just val ->
            String.fromInt val
        Nothing ->
            "NaN"


-- LOGIC


type alias Vector = { x1 : Int
                    , y1 : Int
                    , x2 : Int
                    , y2 : Int
                    }


type alias Space = Dict String Int


defaultContent =
    """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


parseInput : String -> List Vector
parseInput str =
    let
        parseVectors vec =
            case Parser.run parseVector vec of
                Ok pass -> Just pass
                _ -> Nothing
    in
    String.lines str
        |> List.filterMap parseVectors


parseVector : Parser Vector
parseVector =
    succeed Vector
        |= int
        |. symbol ","
        |= int
        |. spaces
        |. symbol "->"
        |. spaces
        |= int
        |. symbol ","
        |= int



solution1 : Model -> Maybe Int
solution1 { input } =
    let
        drawVector vector space =
            vectorToCoordinates1 vector
                |> List.foldl addCoordinatesToSpace space
    in
    input
        |> List.foldl drawVector Dict.empty
        |> calculateSpace
        |> Just


solution2 : Model -> Maybe Int
solution2 { input } =
    let
        drawVector vector space =
            vectorToCoordinates2 vector
                |> List.foldl addCoordinatesToSpace space
    in
    input
        |> List.foldl drawVector Dict.empty
        |> calculateSpace
        |> Just


calculateSpace : Space -> Int
calculateSpace space =
    space
        |> Dict.foldl (\_ v sum -> sum + if v > 1 then 1 else 0) 0


vectorToCoordinates1 : Vector -> List (Int, Int)
vectorToCoordinates1 { x1, y1, x2, y2 } =
    if x1 == x2 then
        List.range (Math.min y1 y2) (Math.max y1 y2)
            |> List.map (\y -> (x1, y))
    else if y1 == y2 then
        List.range (Math.min x1 x2) (Math.max x1 x2)
            |> List.map (\x -> (x, y1))
    else
        []


vectorToCoordinates2 : Vector -> List (Int, Int)
vectorToCoordinates2 { x1, y1, x2, y2 } =
    if x1 == x2 then
        List.range (Math.min y1 y2) (Math.max y1 y2)
            |> List.map (\y -> (x1, y))
    else if y1 == y2 then
        List.range (Math.min x1 x2) (Math.max x1 x2)
            |> List.map (\x -> (x, y1))
    else if Math.abs (x1 - x2) == Math.abs (y1 - y2) then
        List.Extra.zip (Utils.range x1 x2) (Utils.range y1 y2)
    else
        []


addCoordinatesToSpace : (Int, Int) -> Space -> Space
addCoordinatesToSpace coord space =
    let
        set : Maybe Int -> Maybe Int
        set value =
            case value of
                Just val ->
                    Just (val + 1)
                Nothing ->
                    Just 1
    in
    Dict.update (coordToSpaceKey coord) set space


coordToSpaceKey : (Int, Int) -> String
coordToSpaceKey (x, y) =
    String.fromInt x ++ "-" ++ String.fromInt y

