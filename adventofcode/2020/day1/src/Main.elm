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


type alias Pair = (Int, Int)


defaultContent = "1721\n979\n366\n299\n675\n1456"


parseInput : String -> List Int
parseInput str =
    List.filterMap String.toInt (String.lines str)


solution1 : Model -> Int
solution1 { input } =
    case findPair input of
        Just (x, y) -> x * y
        Nothing -> 0


solution2 : Model -> Int
solution2 { input } =
    case findPair input of
        Just (x, y) -> x * y
        Nothing -> 0


findPair : List Int -> Maybe Pair
findPair input =
    case input of
        [] -> Nothing
        x :: [] -> Nothing
        x :: xs ->
            case findElemPair x xs of
                Just pair -> Just pair
                Nothing -> findPair xs
        



findElemPair : Int -> List Int -> Maybe Pair
findElemPair x xs =
    case xs of
        [] -> Nothing
        y :: ys ->
            if x + y == 2020 then
                Just (x, y)
            else
                findElemPair x ys


