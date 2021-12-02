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
  { input : List Move
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


defaultContent = "forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2"


type alias Position =
    { horizontal : Int
    , depth : Int
    , aim : Int
    }


type Move = Forward Int | Down Int | Up Int


parseInput : String -> List Move
parseInput str =
    List.filterMap parseString (String.lines str)


parseString : String -> Maybe Move
parseString str =
    case String.words str of
        x :: y :: [] -> case x of
            "forward" -> case String.toInt y of
                Just val -> Just (Forward val)
                Nothing -> Nothing
            "down" -> case String.toInt y of
                Just val -> Just (Down val)
                Nothing -> Nothing
            "up" -> case String.toInt y of
                Just val -> Just (Up val)
                Nothing -> Nothing
            _ -> Nothing
        _ -> Nothing


solution1 : Model -> Int
solution1 { input } =
    case doMoves input { horizontal = 0, depth = 0, aim = 0 } of
        { horizontal, depth, aim } -> horizontal * depth


solution2 : Model -> Int
solution2 { input } =
    case doNewMoves input { horizontal = 0, depth = 0, aim = 0 } of
        { horizontal, depth, aim } -> horizontal * depth


doMove : Move -> Position -> Position
doMove move position =
    case position of
        { horizontal, depth, aim } -> case move of
            Forward value -> { position | horizontal = horizontal + value }
            Down value -> { position | depth = depth + value }
            Up value -> { position | depth = depth - value }



doNewMove : Move -> Position -> Position
doNewMove move position =
    case position of
        { horizontal, depth, aim } -> case move of
            Forward value -> { position | horizontal = horizontal + value, depth = depth + aim * value }
            Down value -> { position | aim = aim + value }
            Up value -> { position | aim = aim - value }


doMoves : List Move -> Position -> Position
doMoves moves pos =
    List.foldl doMove pos moves


doNewMoves : List Move -> Position -> Position
doNewMoves moves pos =
    List.foldl doNewMove pos moves


