module Main exposing (..)

import Browser
import Html exposing (Html, Attribute, div, textarea, text)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)
import Parser exposing ((|.), (|=), Parser, chompWhile, getChompedString, succeed, symbol)


-- MAIN


main =
  Browser.sandbox { init = init, update = update, view = view }



-- MODEL


type alias Model =
  { input : List Passport
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


type alias Passport = List Field


type alias Field = { key: String
                   , value: String
                   }


defaultContent =
    """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""


parseInput : String -> List Passport
parseInput str =
    String.lines str
        |> groupStrings [] []
        |> List.filter (not << String.isEmpty)
        |> List.map String.words
        |> List.map stringsToPassport
        |> List.filter (not << List.isEmpty)


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


stringsToPassport : List String -> Passport
stringsToPassport strings =
    let
        step =
            \str ->
                case Parser.run parseField str of
                        Ok fld ->
                            if String.isEmpty fld.key || String.isEmpty fld.value then
                                Nothing
                            else
                                Just fld
                        _ -> Nothing
    in
    strings
        |> List.filterMap step


parseField : Parser Field
parseField =
    succeed Field
        |= parseFieldElement
        |. symbol ":"
        |= parseFieldElement


parseFieldElement : Parser String
parseFieldElement =
    succeed ()
        |. chompWhile ((/=) ':')
        |> getChompedString


solution1 : Model -> Int
solution1 { input } =
    let
        step =
            \pass acc ->
                acc + if isValidPassport pass then 1 else 0
    in
    input
        |> List.foldl step 0


solution2 : Model -> Int
solution2 { input } =
    0


isValidPassport : Passport -> Bool
isValidPassport pass =
    containsField "byr" pass
        |> (&&) (containsField "iyr" pass)
        |> (&&) (containsField "eyr" pass)
        |> (&&) (containsField "hgt" pass)
        |> (&&) (containsField "hcl" pass)
        |> (&&) (containsField "ecl" pass)
        |> (&&) (containsField "pid" pass)


containsField : String -> Passport -> Bool
containsField name pass =
    let
        match =
            \compare { key } acc ->
                acc || compare == key
    in
    List.foldl (match name) False pass

