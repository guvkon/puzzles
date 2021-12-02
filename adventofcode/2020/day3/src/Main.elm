module Main exposing (..)

import Array
import Browser
import Html exposing (Html, Attribute, div, textarea, text)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)
import Parser exposing (Parser, (|.), (|=), succeed, symbol, spaces, chompWhile, getChompedString, int)


-- MAIN


main =
  Browser.sandbox { init = init, update = update, view = view }



-- MODEL


type alias Model =
  { input : List Line
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


type alias Line = List Position


type Position = Tree | Open


defaultContent = "..##.......\n#...#...#..\n.#....#..#.\n..#.#...#.#\n.#...##..#.\n..#.##.....\n.#.#.#....#\n.#........#\n#.##...#...\n#...##....#\n.#..#...#.#"


parseInput : String -> List Line
parseInput str =
    List.map parseString (String.lines str)


parseString : String -> Line
parseString str =
    String.toList str
        |> List.map charToPosition


charToPosition : Char -> Position
charToPosition chr =
    case chr of
        '#' -> Tree
        _ -> Open


solution1 : Model -> Int
solution1 { input } =
    walk input


solution2 : Model -> Int
solution2 { input } =
    0


walk : List Line -> Int
walk lines =
    let
        isTree =
            \pos line ->
                case Array.get (modBy (Array.length line) pos) line of
                    Just loc -> case loc of
                        Tree -> True
                        Open -> False
                    Nothing -> False
        step =
            \line (pos, count) ->
                (pos + 3, count + if isTree pos (Array.fromList line) then 1 else 0)
    in
    case lines of
        x :: xs ->
            case List.foldl step (3, 0) xs of
                (_, count) -> count
        _ -> 0


