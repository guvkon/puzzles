module Main exposing (..)

import Basics as Math
import Browser
import Html exposing (Html, Attribute, div, textarea, text)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)
import Matrix
import Parser exposing ((|.), (|=), Parser, int, spaces, succeed, symbol)
import Utils
import List.Extra


-- MAIN


main =
  Browser.sandbox { init = init, update = update, view = view }



-- MODEL


type alias Model =
  { input : List Vector
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
    , div [] [ text ( "Input: " ++ viewModel model ) ]
    , div [] [ text ( "Solution 1: " ++ viewSolution ( solution1 model ) ) ]
    , div [] [ text ( "Solution 2: " ++ viewSolution ( solution2 model ) ) ]
    ]


viewModel : Model -> String
viewModel model =
    (++) "number of vectors = "
        <| (String.fromInt (List.length model.input))


viewSolution : Maybe Int -> String
viewSolution solution =
    case solution of
        Just val ->
            String.fromInt val
        Nothing ->
            "NaN"


-- LOGIC


type alias Vector = { x1 : Int
                    , y1 : Int
                    , x2 : Int
                    , y2 : Int
                    }


type alias Space = Matrix.Matrix Int


defaultContent =
    """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


parseInput : String -> List Vector
parseInput str =
    let
        parseVectors vec =
            case Parser.run parseVector vec of
                Ok pass -> Just pass
                _ -> Nothing
    in
    String.lines str
        |> List.filterMap parseVectors


parseVector : Parser Vector
parseVector =
    succeed Vector
        |= int
        |. symbol ","
        |= int
        |. spaces
        |. symbol "->"
        |. spaces
        |= int
        |. symbol ","
        |= int



solution1 : Model -> Maybe Int
solution1 { input } =
    vectorsToCrossings1 input []
        |> List.Extra.unique
        |> List.length
        |> Just


solution2 : Model -> Maybe Int
solution2 { input } =
    vectorsToCrossings2 input []
            |> List.Extra.unique
            |> List.length
            |> Just


vectorsToCrossings1 : List Vector -> List (Int, Int) -> List (Int, Int)
vectorsToCrossings1 vectors crossings =
    case vectors of
        [] ->
            crossings
        x :: xs ->
            vectorsToCrossings1 xs (crossVectorWithVectors1 x xs crossings)


crossVectorWithVectors1 : Vector -> List Vector -> List (Int, Int) -> List (Int, Int)
crossVectorWithVectors1 vector vectors crossings =
    case vectors of
        [] ->
            crossings
        x :: xs ->
            crossVectorWithVectors1 vector xs (List.append (crossVectors1 vector x) crossings)


crossVectors1 : Vector -> Vector -> List (Int, Int)
crossVectors1 v1 v2 =
    let
        coords : Vector -> List (Int, Int)
        coords { x1, y1, x2, y2 } =
            if x1 == x2 then
                List.range (Math.min y1 y2) (Math.max y1 y2)
                    |> List.map (\y -> (x1, y))
            else if y1 == y2 then
                List.range (Math.min x1 x2) (Math.max x1 x2)
                    |> List.map (\x -> (x, y1))
            else
                []
        coords1 =
            coords v1
        coords2 =
            coords v2
    in
    coords1
        |> List.filterMap (\coord -> if List.member coord coords2 then Just coord else Nothing )


vectorsToCrossings2 : List Vector -> List (Int, Int) -> List (Int, Int)
vectorsToCrossings2 vectors crossings =
    case vectors of
        [] ->
            crossings
        x :: xs ->
            vectorsToCrossings2 xs (crossVectorWithVectors2 x xs crossings)


crossVectorWithVectors2 : Vector -> List Vector -> List (Int, Int) -> List (Int, Int)
crossVectorWithVectors2 vector vectors crossings =
    case vectors of
        [] ->
            crossings
        x :: xs ->
            crossVectorWithVectors2 vector xs (List.append (crossVectors2 vector x) crossings)


crossVectors2 : Vector -> Vector -> List (Int, Int)
crossVectors2 v1 v2 =
    let
        coords : Vector -> List (Int, Int)
        coords { x1, y1, x2, y2 } =
            if x1 == x2 then
                List.range (Math.min y1 y2) (Math.max y1 y2)
                    |> List.map (\y -> (x1, y))
            else if y1 == y2 then
                List.range (Math.min x1 x2) (Math.max x1 x2)
                    |> List.map (\x -> (x, y1))
            else if Math.abs (x1 - x2) == Math.abs (y1 - y2) then
                List.Extra.zip (Utils.range x1 x2) (Utils.range y1 y2)
            else
                []
        coords1 =
            coords v1
        coords2 =
            coords v2
    in
    coords1
        |> List.filterMap (\coord -> if List.member coord coords2 then Just coord else Nothing )

