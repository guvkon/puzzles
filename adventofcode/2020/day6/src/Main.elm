module Main exposing (..)

import Browser
import Html exposing (Html, Attribute, div, textarea, text)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)
import Utils
import List.Extra


-- MAIN


main =
  Browser.sandbox { init = init, update = update, view = view }



-- MODEL


type alias Model =
  { input : List String
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
    (++) "groups size = "
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
    """abc

a
b
c

ab
ac

a
a
a
a

b"""


parseInput : String -> List String
parseInput str =
    Utils.parseStringIntoBlocks str


solution1 : Model -> Maybe Int
solution1 { input } =
    input
        |> List.map (String.lines >> getUniqueAnswers >> List.length)
        |> List.sum
        |> Just


solution2 : Model -> Maybe Int
solution2 { input } =
    Nothing


getUniqueAnswers : List String -> List Char
getUniqueAnswers answers =
    let
        step : String -> List Char -> List Char
        step str acc =
            List.append (String.toList str) acc
    in
    answers
        |> List.foldl step []
        |> List.Extra.unique
