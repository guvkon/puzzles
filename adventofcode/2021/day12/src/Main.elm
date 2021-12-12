module Main exposing (..)

import Basics
import Browser
import Dict
import Html exposing (Html, Attribute, div, a, textarea, text)
import Html.Attributes exposing (class, cols, href, placeholder, rows, target, value)
import Html.Events exposing (onInput)
import Parser exposing ((|.), (|=), Parser, int, spaces, succeed, symbol)
import Utils
import List.Extra


-- MAIN


main =
  Browser.sandbox { init = init, update = update, view = view }



-- MODEL


type alias Model =
  { input : Input
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
               , cols 60
               , class "bg-dark text-white-50 border-1 border-secondary p-2"
               ] []
    , div [] [ a [ href (linkToInput 2021 12)
             , target "_blank"
             , class "text-white-50"
             ] [ text "Link to puzzle's input" ] ]
    , div [] [ text ( "Input: " ++ viewInput model.input ) ]
    , div [] [ text ( "Solution 1: " ++ viewSolution ( solution1 model.input ) ) ]
    , div [] [ text ( "Test 1: " ++ testSolution 10 ( solution1 (parseInput defaultContent) ) ) ]
    , div [] [ text ( "Solution 2: " ++ viewSolution ( solution2 model.input ) ) ]
    , div [] [ text ( "Test 2: " ++ testSolution 226 ( solution2 (parseInput defaultContent) ) ) ]
    ]


viewInput : Input -> String
viewInput input =
    (++) "number of nodes = "
        <| String.fromInt (List.length (Dict.toList (Debug.log "input" input)))


viewSolution : Maybe Int -> String
viewSolution solution =
    case solution of
        Just val ->
            String.fromInt val
        Nothing ->
            "NaN"


testSolution : Int -> Maybe Int -> String
testSolution target result =
    case result of
        Nothing ->
            "Error"
        Just val ->
            if val == target then
                "Passing"
            else
                "Error"


linkToInput : Int -> Int -> String
linkToInput year day =
    "https://adventofcode.com/"
        ++ (String.fromInt year)
        ++ "/day/"
        ++ (String.fromInt day)
        ++ "/input"



-- LOGIC


type alias Input = Cave


type alias Cave = Dict.Dict String (List String)


type alias Rule = { left : String, right : String }



defaultContent =
    """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""


parseInput : String -> Input
parseInput string =
    let
        ruleParser : Parser Rule
        ruleParser =
            succeed Rule
                |= Utils.letters
                |. symbol "-"
                |= Utils.letters

        parseIntoRule : String -> Maybe Rule
        parseIntoRule str =
            case Parser.run ruleParser str of
                Ok value ->
                    Just value
                Err _ ->
                    Nothing

        rules : List Rule
        rules =
            String.trim string
                |> String.lines
                |> List.filterMap parseIntoRule

        addRuleToCave : Rule -> Cave -> Cave
        addRuleToCave rule cave =
            cave
                |> Dict.update rule.left (updateCave rule.right)
                |> Dict.update rule.right (updateCave rule.left)

        updateCave : String -> Maybe (List String) -> Maybe (List String)
        updateCave node nodes =
            case nodes of
                Nothing ->
                    Just (node :: [])
                Just xs ->
                    Just (node :: xs)
    in
    rules
        |> List.foldl addRuleToCave Dict.empty


solution1 : Input -> Maybe Int
solution1 input =
    Nothing


solution2 : Input -> Maybe Int
solution2 input =
    Nothing

