module Main exposing (..)

import Browser
import Html exposing (Html, Attribute, div, textarea, text)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)


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
    [ textarea [ placeholder "Input", value model.content, onInput Change, rows 20, cols 40, class "bg-dark text-light border-1 border-secondary p-2" ] []
    , div [] [ text ( "Input size: " ++ String.fromInt ( List.length model.input ) ) ]
    , div [] [ text ( "Solution 1: " ++ String.fromInt ( solution1 model ) ) ]
    , div [] [ text ( "Solution 2: " ++ String.fromInt ( solution2 model ) ) ]
    ]


-- LOGIC


defaultContent = "199\n200\n208\n210\n200\n207\n240\n269\n260\n263"


parseInput : String -> List Int
parseInput str =
    List.filterMap String.toInt (String.lines str)


solution1 : Model -> Int
solution1 model =
    increases model.input


solution2 : Model -> Int
solution2 model =
    increases (averageInput model.input)


increases : List Int -> Int
increases input =
    List.sum (List.map2 increase (takes 1 input) (List.drop 1 input))


increase : Int -> Int -> Int
increase prev next =
    if next > prev then
        1
    else
        0


takes : Int -> List Int -> List Int
takes amount list =
    List.take (List.length list - amount) list


averageInput : List Int -> List Int
averageInput input =
    List.map3 (\a b c -> a + b + c) (takes 2 input) (List.drop 1 (takes 1 input)) (List.drop 2 input)


