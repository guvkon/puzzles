module Main exposing (..)

import Browser
import Html exposing (Html, Attribute, div, textarea, text)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)
import Parser exposing ((|.), (|=), Parser, int, succeed, symbol)
import Utils exposing (letters, stringEntry)


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


type alias Height = { value : Int
                    , metric : String
                    }


type alias HairColor = { color : String }


defaultContent =
    """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719

eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""


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
        |= (stringEntry ((/=) ':'))
        |. symbol ":"
        |= (stringEntry ((/=) ':'))


solution1 : Model -> Int
solution1 { input } =
    countValidPassports isValidPassport1 input


solution2 : Model -> Int
solution2 { input } =
    countValidPassports isValidPassport2 input


countValidPassports : (Passport -> Bool) -> List Passport -> Int
countValidPassports check passports =
    let
        step =
            \pass acc ->
                acc + if check pass then 1 else 0
    in
    passports
        |> List.foldl step 0


isValidPassport1 : Passport -> Bool
isValidPassport1 pass =
    containsField "byr" pass
        |> (&&) (containsField "iyr" pass)
        |> (&&) (containsField "eyr" pass)
        |> (&&) (containsField "hgt" pass)
        |> (&&) (containsField "hcl" pass)
        |> (&&) (containsField "ecl" pass)
        |> (&&) (containsField "pid" pass)


isValidPassport2 : Passport -> Bool
isValidPassport2 pass =
    checkByr pass
        |> (&&) (checkIyr pass)
        |> (&&) (checkEyr pass)
        |> (&&) (checkHgt pass)
        |> (&&) (checkHcl pass)
        |> (&&) (checkEcl pass)
        |> (&&) (checkPid pass)


checkByr : Passport -> Bool
checkByr pass =
    getField "byr" pass
        |> isNumberInRange 1920 2002


checkIyr : Passport -> Bool
checkIyr pass =
    getField "iyr" pass
        |> isNumberInRange 2010 2020


checkEyr : Passport -> Bool
checkEyr pass =
    getField "eyr" pass
        |> isNumberInRange 2020 2030


isNumberInRange : Int -> Int -> Maybe String -> Bool
isNumberInRange min max str =
    case str of
        Just value ->
            case String.toInt value of
                Just num ->
                    min <= num && num <= max
                Nothing ->
                    False
        Nothing ->
            False


checkHgt : Passport -> Bool
checkHgt pass =
    case getField "hgt" pass of
        Just value ->
            case Parser.run parseHgt value of
                Ok hgt ->
                    case hgt.metric of
                        "cm" ->
                            150 <= hgt.value && hgt.value <= 193
                        "in" ->
                            59 <= hgt.value && hgt.value <= 76
                        _ ->
                            False
                _ ->
                    False
        Nothing ->
            False


parseHgt : Parser Height
parseHgt =
    succeed Height
        |= int
        |= letters


checkHcl : Passport -> Bool
checkHcl pass =
    case getField "hcl" pass of
        Just value ->
            case Parser.run parseHcl value of
                Ok { color } ->
                    let
                        check =
                            \chr acc ->
                                acc && Char.isHexDigit chr
                        hexes =
                            String.toList color
                    in
                    List.foldl check True hexes
                        |> (&&) (List.length hexes == 6)
                _ ->
                    False
        Nothing ->
            False


parseHcl : Parser HairColor
parseHcl =
    succeed HairColor
        |. symbol "#"
        |= (stringEntry Char.isHexDigit)


checkEcl : Passport -> Bool
checkEcl pass =
    case getField "ecl" pass of
        Just value ->
            List.member value ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        Nothing ->
            False


checkPid : Passport -> Bool
checkPid pass =
    case getField "pid" pass of
        Just value ->
            let
                check =
                    \chr acc ->
                        acc && Char.isDigit chr
                digits =
                    String.toList value
            in
            List.length digits == 9
                |> (&&) (List.foldl check True digits)
        Nothing ->
            False


getField : String -> Passport -> Maybe String
getField name pass =
    let
        get =
            \compare { key, value } acc ->
                if acc /= Nothing then
                    acc
                else if key == compare then
                    Just value
                else
                    Nothing
    in
    List.foldl (get name) Nothing pass


containsField : String -> Passport -> Bool
containsField name pass =
    case getField name pass of
        Just _ -> True
        Nothing -> False

