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


type alias Board = { id : String
                   , board : List (List Field)
                   }


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
            let
                board =
                    String.lines string
                        |> List.map parseRow
            in
            { id = string, board = board }
        parseBoards : List String -> List Board
        parseBoards strings =
            strings
                |> List.map parseBoard
    in
    case Utils.parseStringIntoBlocks str of
        [] ->
            { numbers = [], boards = [] }
        x :: xs ->
            { numbers = parseNumbers x, boards = parseBoards xs }


solution1 : Model -> Int
solution1 { input } =
    let
        maybeWinner =
            playBingo input.numbers input.boards
    in
    case maybeWinner of
        Nothing ->
            -1
        Just winner ->
            case winner of
                (number, board) ->
                    calculateWinnerBoardScore number board


solution2 : Model -> Int
solution2 { input } =
    let
        winners =
            findAllWinners input.numbers input.boards []
        winnerScores =
            List.map calculateScore winners
    in
    case List.head winnerScores of
        Nothing ->
            -1
        Just score ->
            score


calculateScore : (Int, Board) -> Int
calculateScore (number, board) =
    calculateWinnerBoardScore number board


playBingo : List Int -> List Board -> Maybe (Int, Board)
playBingo numbers boards =
    findAllWinners numbers boards []
        |> List.reverse
        |> List.head


findAllWinners : List Int -> List Board -> List (Int, Board) -> List (Int, Board)
findAllWinners numbers boards winners =
    case numbers of
        [] ->
            winners
        x :: xs ->
            let
                markedBoards =
                    markBoards x boards
                winnerBoards =
                    findWinnerBoards markedBoards
                newWinners =
                    winnerBoards
                        |> List.map (\winner -> (x, winner))
                remainingBoards =
                    pluckBoards (List.map (\board -> board.id) winnerBoards) markedBoards
            in
            List.append newWinners winners
                |> findAllWinners xs remainingBoards


pluckBoards : List String -> List Board -> List Board
pluckBoards ids boards =
    case ids of
        [] ->
            boards
        x :: xs ->
            pluckBoard x boards
                |> pluckBoards xs


pluckBoard : String -> List Board -> List Board
pluckBoard id boards =
    boards
        |> List.filter (\board -> board.id /= id)


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
        markBoard board =
            { board | board = List.map markRow board.board}
    in
    List.map markBoard boards


calculateWinnerBoardScore : Int -> Board -> Int
calculateWinnerBoardScore num { board } =
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


findWinnerBoards : List Board -> List Board
findWinnerBoards boards =
    boards
        |> List.filter (\board -> hasBoardWon board)


hasBoardWon : Board -> Bool
hasBoardWon { board } =
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

