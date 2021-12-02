module Main exposing (..)

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
  { input : List Password
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


type alias Password =
    { min : Int
    , max : Int
    , symbol : String
    , pass : String
    }


defaultContent = "1-3 a: abcde\n1-3 b: cdefg\n2-9 c: ccccccccc"


parseInput : String -> List Password
parseInput str =
    List.filterMap parseString (String.lines str)


parseString : String -> Maybe Password
parseString str =
    case Parser.run password str of
        Ok pass -> Just pass
        _ -> Nothing


password : Parser Password
password =
    succeed Password
        |= int
        |. symbol "-"
        |= int
        |. spaces
        |= letters
        |. symbol ":"
        |. spaces
        |= letters


letters : Parser String
letters =
    succeed ()
        |. chompWhile Char.isAlpha
        |> getChompedString


solution1 : Model -> Int
solution1 { input } =
    countValidPasswords input


solution2 : Model -> Int
solution2 { input } =
    0


countValidPasswords : List Password -> Int
countValidPasswords passwords =
    passwords
        |> List.foldl (\pass count -> count + if validPassword pass then 1 else 0) 0


validPassword : Password -> Bool
validPassword { min, max, symbol, pass } =
    let
        inclusions =
            String.indexes symbol pass
                |> List.length
    in
    if min <= inclusions && max >= inclusions then
        True
    else
        False


