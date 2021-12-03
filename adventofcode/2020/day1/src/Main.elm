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


type alias Triple = (Int, Int, Int)


defaultContent = "1721\n979\n366\n299\n675\n1456"


parseInput : String -> List Int
parseInput str =
    String.lines str
        |> List.filterMap String.toInt


solution1 : Model -> Int
solution1 { input } =
    case findPair input 2020 of
        Just (x, y) -> x * y
        Nothing -> -1


solution2 : Model -> Int
solution2 { input } =
    case findTriple input 2020 of
        Just (x, y, z) -> x * y * z
        Nothing -> -1


findPair : List Int -> Int -> Maybe Pair
findPair input target =
    case input of
        [] -> Nothing
        x :: [] -> Nothing
        x :: xs ->
            case findElemPair x xs target of
                Just y -> Just (x, y)
                Nothing -> findPair xs target
        



findElemPair : Int -> List Int -> Int -> Maybe Int
findElemPair x xs target =
    case xs of
        [] -> Nothing
        y :: ys ->
            if x + y == target then
                Just y
            else
                findElemPair x ys target


findTriple : List Int -> Int -> Maybe Triple
findTriple input target =
    case input of
        [] -> Nothing
        _ :: [] -> Nothing
        _ :: _ :: [] -> Nothing
        x :: xs ->
            case findPair xs (target - x) of
                Just (y, z) -> Just (x, y, z)
                Nothing -> findTriple xs target


