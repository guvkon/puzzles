module Main exposing (..)

import Basics
import Browser
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
  { input : List Int
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
               , class "bg-dark text-white-50 border-1 border-secondary p-2"
               ] []
    , div [] [ a [ href (linkToInput 2021 7)
             , target "_blank"
             , class "text-white-50"
             ] [ text "Link to puzzle's input" ] ]
    , div [] [ text ( "Input: " ++ viewModel model ) ]
    , div [] [ text ( "Solution 1: " ++ viewSolution ( solution1 model ) ) ]
    , div [] [ text ( "Test 1: " ++ testSolution 37 ( solution1 model ) ) ]
    , div [] [ text ( "Solution 2: " ++ viewSolution ( solution2 model ) ) ]
    , div [] [ text ( "Test 2: " ++ testSolution 168 ( solution2 model ) ) ]
    ]


viewModel : Model -> String
viewModel model =
    (++) "amount of crabs = "
        <| (String.fromInt (List.length model.input))


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


defaultContent =
    """16,1,2,0,4,2,7,1,2,14"""


parseInput : String -> List Int
parseInput str =
    String.trim str
        |> String.split ","
        |> List.filterMap String.toInt


solution1 : Model -> Maybe Int
solution1 { input } =
    solve calculateFuel1 input


solution2 : Model -> Maybe Int
solution2 { input } =
    solve calculateFuel2 input


solve : (Int -> List Int -> Int) -> List Int -> Maybe Int
solve calculateFuel input =
    let
        positions =
            List.range (Maybe.withDefault 0 (List.minimum input)) (Maybe.withDefault 0 (List.maximum input))
    in
    case positions of
        [] ->
            Nothing
        x :: xs ->
            let
                step pos fuel =
                    min fuel (calculateFuel pos input)
            in
            List.foldl step (calculateFuel x input) xs
                |> Just


calculateFuel1 : Int -> List Int -> Int
calculateFuel1 moveTo positions =
    positions
        |> List.foldl (\pos sum -> sum + (abs (moveTo - pos))) 0


calculateFuel2 : Int -> List Int -> Int
calculateFuel2 moveTo positions =
    let
        len pos =
            abs (moveTo - pos)
        step pos sum =
            let
                n =
                    len pos
            in
            sum + ((n + 1) * n // 2)
    in
    positions
        |> List.foldl step 0
