module Main exposing (..)

import Basics as Math
import Browser
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
    (++) "amount of numbers = "
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
    """3,4,3,1,2"""


parseInput : String -> List Int
parseInput str =
    String.split "," str
        |> List.filterMap String.toInt


solution1 : Model -> Maybe Int
solution1 { input } =
    let
        step : a -> List Int -> List Int
        step _ acc =
            List.map nextDay acc
                |> List.concat
    in
    List.range 0 79
        |> List.foldl step input
        |> List.length
        |> Just


solution2 : Model -> Maybe Int
solution2 { input } =
    Nothing


nextDay : Int -> List Int
nextDay num =
    case num of
        0 ->
            [6, 8]
        x ->
            [x - 1]
