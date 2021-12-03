module Main exposing (..)

import Array
import Browser
import Html exposing (Html, Attribute, div, textarea, text)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)
import Binary


-- MAIN


main =
  Browser.sandbox { init = init, update = update, view = view }



-- MODEL


type alias Model =
  { input : List (List Int)
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


defaultContent = "00100\n11110\n10110\n10111\n10101\n01111\n00111\n11100\n10000\n11001\n00010\n01010"


parseInput : String -> List (List Int)
parseInput str =
    List.map (\line -> List.filterMap (\char -> String.toInt (String.fromChar char)) (String.toList line)) (String.lines str)


solution1 : Model -> Int
solution1 { input } =
    let
        hrzInput =
            horizontalInput input
    in
    gammaRate hrzInput
        |> (*) (epsilonRate hrzInput)


solution2 : Model -> Int
solution2 model =
    0


horizontalInput : List (List Int) -> List (List Int)
horizontalInput input =
    case input of
        x :: xs ->
            List.map (\(idx, _) -> List.map (getElem idx) input) (Array.toIndexedList (Array.fromList x))
        [] -> []


getElem : Int -> List Int -> Int
getElem index line =
    case Array.get index (Array.fromList line) of
        Just val -> val
        Nothing -> 0


gammaRate : List (List Int) -> Int
gammaRate hrzInput =
    let
        bit =
            \list ->
                if List.sum list > List.length list // 2 then
                    1
                else
                    0
        bits =
            \input ->
                List.map bit input
    in
    Binary.toDecimal (Binary.fromIntegers (bits hrzInput))


epsilonRate : List (List Int) -> Int
epsilonRate hrzInput =
    let
        bit =
            \list ->
                if List.sum list < List.length list // 2 then
                    1
                else
                    0
        bits =
            \input ->
                List.map bit input
    in
    Binary.toDecimal (Binary.fromIntegers (bits hrzInput))
    


