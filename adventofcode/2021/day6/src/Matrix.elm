module Matrix exposing (Matrix, get, set, updateAt, updateIfIndex, indexedMap, map, init, toList, width, height)

import List.Extra


type alias Matrix a = { width : Int
                    , height : Int
                    , values : List a
                    }


init : Int -> Int -> a -> Matrix a
init w h value =
    { width = w
    , height = h
    , values = List.repeat (w * h) value
    }


toList : Matrix a -> List a
toList matrix =
    matrix.values


width : Matrix a -> Int
width matrix =
    matrix.width


height : Matrix a -> Int
height matrix =
    matrix.height


get : (Int, Int) -> Matrix a -> Maybe a
get (x, y) matrix =
    let
        index =
            x * matrix.width + y * matrix.height
    in
    List.Extra.getAt index matrix.values


set : (Int, Int) -> a -> Matrix a -> Matrix a
set idx value matrix =
    updateAt idx (\_ -> value) matrix


updateAt : (Int, Int) -> (a -> a) -> Matrix a -> Matrix a
updateAt (x, y) func matrix =
    let
        index =
            x * matrix.width + y * matrix.height
    in
    { matrix | values = List.Extra.updateAt index func matrix.values }


updateIfIndex : ((Int, Int) -> Bool) -> (a -> a) -> Matrix a -> Matrix a
updateIfIndex ifIndex func matrix =
    let
        step (idx, val) =
            if ifIndex idx then
                func val
            else
                val
    in
    indexedMap step matrix


map : (a -> a) -> Matrix a -> Matrix a
map func matrix =
    { matrix | values = List.map func matrix.values }


indexedMap : (((Int, Int), a) -> a) -> Matrix a -> Matrix a
indexedMap func matrix  =
    let
        nextIndex : (Int, Int) -> (Int, Int)
        nextIndex idx =
            case idx of
                (xx, yy) ->
                    if yy == matrix.width - 1 then
                        (xx + 1, 0)
                    else
                        (xx, yy + 1)
        indexesStep acc _ =
            (nextIndex acc, nextIndex acc)
        indexes =
            case List.Extra.mapAccuml indexesStep (0, -1) matrix.values of
                (_, list) ->
                    list
        step : (Int, Int) -> a -> a
        step idx val =
            func (idx, val)
    in
    { matrix | values = List.map2 step indexes matrix.values }

