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
  { input : Bingo
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
    , div [] [ text ( "Count numbers: " ++ String.fromInt ( List.length model.input.numbers ) ) ]
    , div [] [ text ( "Count boards: " ++ String.fromInt ( List.length model.input.boards ) ) ]
    , div [] [ text ( "Solution 1: " ++ String.fromInt ( solution1 model ) ) ]
    , div [] [ text ( "Solution 2: " ++ String.fromInt ( solution2 model ) ) ]
    ]


-- LOGIC


type alias Bingo = { numbers : List Int
                   , boards : List Board
                   }


type alias Board = List (List Field)


type alias Field = (Int, Bool)


defaultContent =
    """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
8  2 23  4 24
21  9 14 16  7
6 10  3 18  5
1 12 20 15 19

3 15  0  2 22
9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
2  0 12  3  7"""


parseInput : String -> Bingo
parseInput str =
    let
        groupedStrings =
            String.lines str
                    |> groupStrings [] []
                    |> List.filter (not << String.isEmpty)
                    |> List.reverse
        parseNumbers : String -> List Int
        parseNumbers string =
            String.split "," string
                |> List.filterMap String.toInt
        parseField : String -> Maybe Field
        parseField string =
            case String.toInt string of
                Nothing ->
                    Nothing
                Just val ->
                    Just (val, False)
        parseRow : String -> List Field
        parseRow string =
            String.words string
                |> List.filterMap parseField
        parseBoard : String -> Board
        parseBoard string =
            String.lines string
                |> List.map parseRow
        parseBoards : List String -> List Board
        parseBoards strings =
            strings
                |> List.map parseBoard
    in
    case groupedStrings of
        [] ->
            { numbers = [], boards = [] }
        x :: xs ->
            { numbers = parseNumbers x, boards = parseBoards xs }


groupStrings : List String -> List String -> List String -> List String
groupStrings temp result rawList =
    let
        append =
            \y ys ->
                String.join "\n" y :: ys
    in
    case rawList of
        x :: xs ->
            if x == "" then
                groupStrings [] (append temp result) xs
            else
                groupStrings (x :: temp) result xs
        [] -> append temp result


solution1 : Model -> Int
solution1 { input } =
    let
        maybeWinner =
            playBingo input.numbers input.boards
    in
    case maybeWinner of
        Nothing ->
            0
        Just winner ->
            case winner of
                (number, board) ->
                    calculateWinnerBoardScore number board



solution2 : Model -> Int
solution2 { input } =
    0


playBingo : List Int -> List Board -> Maybe (Int, Board)
playBingo numbers boards =
    case numbers of
        [] ->
            Nothing
        x :: xs ->
            let
                markedBoards =
                    markBoards x boards
                winnerBoard =
                    findWinnerBoard markedBoards
            in
            case winnerBoard of
                Just board ->
                    Just (x, board)
                Nothing ->
                    playBingo xs markedBoards


markBoards : Int -> List Board -> List Board
markBoards number boards =
    let
        markField =
            \(val, marked) ->
                if val == number then
                    (val, True)
                else
                    (val, marked)
        markRow =
            \row ->
                List.map markField row
        markBoard =
            \board ->
                List.map markRow board
    in
    List.map markBoard boards


calculateWinnerBoardScore : Int -> Board -> Int
calculateWinnerBoardScore num board =
    let
        unmarkedRowSum : Field -> Int -> Int
        unmarkedRowSum =
            \(val, marked) sum ->
                sum + if marked then 0 else val
        unmarkedSum : List Field -> Int -> Int
        unmarkedSum =
            \row sum ->
                sum + List.foldl unmarkedRowSum 0 row
        score =
            List.foldl unmarkedSum 0 board
    in
    num * score



findWinnerBoard : List Board -> Maybe Board
findWinnerBoard boards =
    let
        step : Board -> Maybe Board -> Maybe Board
        step =
            \board acc ->
                case acc of
                    Just val ->
                        Just val
                    Nothing ->
                        if hasBoardWon board then
                            Just board
                        else
                            Nothing
    in
    boards
        |> List.foldl step Nothing



hasBoardWon : Board -> Bool
hasBoardWon board =
    let
        rowWon : Field -> Bool -> Bool
        rowWon =
            \(_, marked) won ->
                won && marked
        boardWon : List Field -> Bool -> Bool
        boardWon =
            \row won ->
                won || List.foldl rowWon True row
        rotatedBoard =
            Utils.rotateMatrix board
        megaBoard =
            List.append board rotatedBoard
    in
    megaBoard
        |> List.foldl boardWon False
