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
    let
        space =
            produceSpace input
        step =
            Utils.counter (\x -> x >= 2)
    in
    space
        |> applyVectors input
        |> Matrix.toList
        |> List.foldl step 0
        |> Just


solution2 : Model -> Maybe Int
solution2 { input } =
    Nothing


produceSpace : List Vector -> Space
produceSpace vectors =
    let
        xs =
            vectors
                |> List.map (\vec -> [vec.x1, vec.x2])
                |> List.concat
        ys =
            vectors
                |> List.map (\vec -> [vec.y1, vec.y2])
                |> List.concat
        width =
            1 + (Maybe.withDefault -1 (List.maximum xs))
        height =
            1 + (Maybe.withDefault -1 (List.maximum ys))
    in
    Matrix.init width height 0


applyVectors : List Vector -> Space -> Space
applyVectors vectors space =
    vectors
        |> List.foldl applyVector space


applyVector : Vector -> Space -> Space
applyVector { x1, y1, x2, y2 } space =
    let
        step : ((Int, Int), Int) -> Int
        step (idx, val) =
            case idx of
                (x, y) ->
                    if x1 == x2 then
                        let
                            minY = Math.min y1 y2
                            maxY = Math.max y1 y2
                        in
                        if x == x1 && minY <= y && y <= maxY then
                            val + 1
                        else
                            val
                    else if y1 == y2 then
                        let
                            minX = Math.min x1 x2
                            maxX = Math.max x1 x2
                        in
                        if y == y1 && minX <= x && x <= maxX then
                            val + 1
                        else
                            val
                    else
                        val
    in
    Matrix.indexedMap step space

