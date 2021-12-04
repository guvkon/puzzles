module Main exposing (..)

import Browser
import Html exposing (Html, Attribute, div, textarea, text)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)
import Utils exposing (decimal, indexes, element)


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
    [ textarea [ placeholder "Input"
               , value model.content
               , onInput Change
               , rows 20
               , cols 40
               , class "bg-dark text-light border-1 border-secondary p-2"
               ] []
    , div [] [ text ( "Input size: " ++ String.fromInt ( List.length model.input ) ) ]
    , div [] [ text ( "Solution 1: " ++ String.fromInt ( solution1 model ) ) ]
    , div [] [ text ( "Solution 2: " ++ String.fromInt ( solution2 model ) ) ]
    ]


-- LOGIC


defaultContent = "00100\n11110\n10110\n10111\n10101\n01111\n00111\n11100\n10000\n11001\n00010\n01010"


parseInput : String -> List (List Int)
parseInput str =
    let
        parseBit =
            \char ->
                String.fromChar char
                    |> String.toInt
        step =
            \line ->
                String.toList line
                    |> List.filterMap parseBit
    in
    String.lines str
        |> List.map step


rotateInput : List (List a) -> List (List a)
rotateInput input =
    let
        step =
            \index ->
                List.filterMap (element index) input
    in
    case input of
        x :: _ ->
            indexes x
                |> List.map step
        [] -> []


solution1 : Model -> Int
solution1 { input } =
    let
        hrzInput =
            rotateInput input
    in
    gammaRate hrzInput
        |> (*) (epsilonRate hrzInput)


solution2 : Model -> Int
solution2 { input } =
    oxygenRating 0 input
        |> (*) (co2Rating 0 input)


gammaRate : List (List Int) -> Int
gammaRate hrzInput =
    genericRating1 (mostCommonBit 0) hrzInput


epsilonRate : List (List Int) -> Int
epsilonRate hrzInput =
    genericRating1 (leastCommonBit 0) hrzInput


genericRating1 : (List Int -> Int) -> List (List Int) -> Int
genericRating1 compare hrzInput =
    List.map compare hrzInput
        |> decimal


oxygenRating : Int -> List (List Int) -> Int
oxygenRating index input =
    genericRating2 (mostCommonBit 1) index input


co2Rating : Int -> List (List Int) -> Int
co2Rating index input =
    genericRating2 (leastCommonBit 0) index input


genericRating2 : (List Int -> Int) -> Int -> List (List Int) -> Int
genericRating2 compare index input =
    case input of
        [] -> 0
        x :: [] ->
            decimal x
        x :: _ ->
            case element index (rotateInput input)  of
                Just line ->
                    let
                        bit =
                            compare line
                        filter =
                            \num ->
                                case element index num of
                                    Just val ->
                                        val == bit
                                    Nothing ->
                                        False
                    in
                    List.filter filter input
                        |> genericRating2 compare (index + 1)
                Nothing ->
                    decimal x


mostCommonBit : Int -> List Int -> Int
mostCommonBit default list =
    case commonBit list of
        One -> 1
        Zero -> 0
        Neither -> default


leastCommonBit : Int -> List Int -> Int
leastCommonBit default list =
    case commonBit list of
        One -> 0
        Zero -> 1
        Neither -> default


type CommonBit = Zero | One | Neither


commonBit : List Int -> CommonBit
commonBit list =
    let
        ones =
            List.sum list
        zeroes =
            List.length list - ones
    in
    if ones == zeroes then
        Neither
    else if ones > zeroes then
        One
    else
        Zero

