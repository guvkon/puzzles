module Main exposing (..)

import Browser
import Html exposing (Html, Attribute, div, textarea, text)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)
import Utils


-- MAIN


main =
  Browser.sandbox { init = init, update = update, view = view }



-- MODEL


type alias Model =
  { input : List BoardingPass
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
    , div [] [ text ( "Input size: " ++ String.fromInt ( List.length model.input ) ) ]
    , div [] [ text ( "Solution 1: " ++ String.fromInt ( solution1 model ) ) ]
    , div [] [ text ( "Solution 2: " ++ String.fromInt ( solution2 model ) ) ]
    ]


-- LOGIC


type alias BoardingPass = { row: List Int
                          , col: List Int
                          }


defaultContent =
    """BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL"""


parseInput : String -> List BoardingPass
parseInput str =
    let
        toBit =
            \chr ->
                case chr of
                    'F' -> 0
                    'B' -> 1
                    'L' -> 0
                    'R' -> 1
                    _ -> 0
        toPass =
            \bits ->
                { row = List.take 7 bits, col = List.drop 7 bits }
    in
    String.lines str
        |> List.map String.toList
        |> List.map (List.map toBit)
        |> List.map toPass


solution1 : Model -> Int
solution1 { input } =
    let
        maybeMax =
            List.map seatId input
                |> List.maximum
    in
    case maybeMax of
        Just val -> val
        Nothing -> -1



solution2 : Model -> Int
solution2 { input } =
    List.map seatId input
        |> List.sort
        |> findMissing


findMissing : List Int -> Int
findMissing ids =
    case ids of
        [] ->
            0
        _ :: [] ->
            0
        x :: y :: xs ->
            if x + 1 /= y then
                x + 1
            else
                findMissing (y :: xs)


seatId : BoardingPass -> Int
seatId { col, row } =
    (Utils.decimal row) * 8 + (Utils.decimal col)

