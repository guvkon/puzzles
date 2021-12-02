module Main exposing (..)

import Browser
import Html exposing (Html, Attribute, div, textarea, text)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)
import ParseInt exposing (parseInt, toRadix)


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
  { input = []
  , content = ""
  }



-- UPDATE


type Msg
  = Change String


update : Msg -> Model -> Model
update msg model =
  case msg of
    Change newContent ->
      { model | content = newContent, input = parseInput newContent }


parseInput : String -> List Int
parseInput str =
    List.filter isPositive (List.map parseIntAlways (String.lines str))


isPositive : Int -> Bool
isPositive val =
    if val > 0 then
        True
    else
        False


parseIntAlways : String -> Int
parseIntAlways str =
    case parseInt str of
        Ok val -> val
        Err _ -> 0



-- VIEW


view : Model -> Html Msg
view model =
  div []
    [ textarea [ placeholder "Input", value model.content, onInput Change, rows 40, cols 100 ] []
    , div [] [ text ("Input size: " ++ String.fromInt (List.length model.input)) ]
    , div [] [ text ("Number of increases: " ++ String.fromInt (increases model.input)) ]
    , div [] [ text ("Number of increases with less noise: " ++ String.fromInt (increases (averageInput model.input))) ]
    ]


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
    List.map3 average (takes 2 input) (List.drop 1 (takes 1 input)) (List.drop 2 input)


average : Int -> Int -> Int -> Int
average a b c =
    a + b + c
