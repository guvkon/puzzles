module Main exposing (..)

import Basics
import Browser
import Html exposing (Html, Attribute, div, textarea, text)
import Html.Attributes exposing (placeholder, value, cols, rows, class)
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
               , class "bg-secondary text-light border-1 border-dark p-2"
               ] []
    , div [] [ text ( "Input: " ++ viewModel model ) ]
    , div [] [ text ( "Solution 1: " ++ viewSolution ( solution1 model ) ) ]
    , div [] [ text ( "Solution 2: " ++ viewSolution ( solution2 model ) ) ]
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
