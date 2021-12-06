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
  { input : List Int
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
    (++) "amount of numbers = "
        <| (String.fromInt (List.length model.input))


viewSolution : Maybe Int -> String
viewSolution solution =
    case solution of
        Just val ->
            String.fromInt val
        Nothing ->
            "NaN"


-- LOGIC


type alias Cluster = { f0 : Int
                     , f1 : Int
                     , f2 : Int
                     , f3 : Int
                     , f4 : Int
                     , f5 : Int
                     , f6 : Int
                     , f7 : Int
                     , f8 : Int
                     }


defaultContent =
    """3,4,3,1,2"""


parseInput : String -> List Int
parseInput str =
    String.split "," str
        |> List.filterMap String.toInt


solution1 : Model -> Maybe Int
solution1 { input } =
    solve 80 input


solution2 : Model -> Maybe Int
solution2 { input } =
    solve 256 input


solve : Int -> List Int -> Maybe Int
solve days fish =
    let
        countCluster cluster =
            case cluster of
                { f0, f1, f2, f3, f4, f5, f6, f7, f8 } ->
                    f0 + f1 + f2 + f3 + f4 + f5 + f6 + f7 + f8
    in
    List.range 0 (days - 1)
        |> List.foldl (\_ cl -> nextDay cl) (clusterise fish)
        |> countCluster
        |> Just


nextDay : Cluster -> Cluster
nextDay cluster =
    case cluster of
        { f0, f1, f2, f3, f4, f5, f6, f7, f8 } ->
            { f0 = f1
            , f1 = f2
            , f2 = f3
            , f3 = f4
            , f4 = f5
            , f5 = f6
            , f6 = f7 + f0
            , f7 = f8
            , f8 = f0
            }


clusterise : List Int -> Cluster
clusterise fish =
    let
        zeroCluster =
            { f0 = 0
            , f1 = 0
            , f2 = 0
            , f3 = 0
            , f4 = 0
            , f5 = 0
            , f6 = 0
            , f7 = 0
            , f8 = 0
            }
    in
    fish
        |> List.foldl (\f cluster -> addFishToCluster f cluster) zeroCluster


addFishToCluster : Int -> Cluster -> Cluster
addFishToCluster fish cluster =
    case cluster of
        { f0, f1, f2, f3, f4, f5, f6, f7, f8 } ->
            { f0 = f0 + if fish == 0 then 1 else 0
            , f1 = f1 + if fish == 1 then 1 else 0
            , f2 = f2 + if fish == 2 then 1 else 0
            , f3 = f3 + if fish == 3 then 1 else 0
            , f4 = f4 + if fish == 4 then 1 else 0
            , f5 = f5 + if fish == 5 then 1 else 0
            , f6 = f6 + if fish == 6 then 1 else 0
            , f7 = f7 + if fish == 7 then 1 else 0
            , f8 = f8 + if fish == 8 then 1 else 0
            }

