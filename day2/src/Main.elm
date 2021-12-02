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
  { input : List Move
  , content : String
  }


defaultContent = "forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2"


init : Model
init =
  { input = parseInput defaultContent
  , content = defaultContent
  }


type alias Position =
    { horizontal : Int
    , depth : Int
    , aim : Int
    }


type Move = Forward Int | Down Int | Up Int | Stay


stringToMove : String -> Move
stringToMove str =
    case String.words str of
        x :: y :: xs -> case x of
            "forward" -> Forward (parseIntAlways y)
            "down" -> Down (parseIntAlways y)
            "up" -> Up (parseIntAlways y)
            _ -> Stay
        x :: xs -> Stay
        [] -> Stay


doMove : Move -> Position -> Position
doMove move position =
    case position of
        { horizontal, depth, aim } -> case move of
            Forward value -> { position | horizontal = horizontal + value }
            Down value -> { position | depth = depth + value }
            Up value -> { position | depth = depth - value }
            Stay -> position



doNewMove : Move -> Position -> Position
doNewMove move position =
    case position of
        { horizontal, depth, aim } -> case move of
            Forward value -> { position | horizontal = horizontal + value, depth = depth + aim * value }
            Down value -> { position | aim = aim + value }
            Up value -> { position | aim = aim - value }
            Stay -> position


doMoves : List Move -> Position -> Position
doMoves moves pos =
    List.foldl doMove pos moves


doNewMoves : List Move -> Position -> Position
doNewMoves moves pos =
    List.foldl doNewMove pos moves


solution : List Move -> Int
solution input =
    case doMoves input { horizontal = 0, depth = 0, aim = 0 } of
        { horizontal, depth, aim } -> horizontal * depth


solution2 : List Move -> Int
solution2 input =
    case doNewMoves input { horizontal = 0, depth = 0, aim = 0 } of
        { horizontal, depth, aim } -> horizontal * depth


-- UPDATE


type Msg
  = Change String


update : Msg -> Model -> Model
update msg model =
  case msg of
    Change newContent ->
      { model | content = newContent, input = parseInput newContent }


parseInput : String -> List Move
parseInput str =
    List.map stringToMove (String.lines str)


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
    , div [] [ text ("Solution 1: " ++ String.fromInt (solution model.input)) ]
    , div [] [ text ("Solution 2: " ++ String.fromInt (solution2 model.input)) ]
    ]


