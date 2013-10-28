<?php
/**
 * PHP REST Wrapper, outputs JSON Wrapper for MPD control
 *
 * http://192.168.1.7/mpd/index.php?cmd=getPlaylist
 * http://192.168.1.7/mpd/index.php?cmd=searchArtist&artist=plump
 */
ini_set('display_errors', true);
error_reporting(E_ALL | E_STRICT);
require_once 'Net/MPD.php';

class mpdController {
  protected $MPD_DB = null;
  protected $MPD_PLS = null;
  protected $MPD_PLY = null;
  
  public function __construct() {
    $this->MPD_DB = Net_MPD::factory('Database');
    $this->MPD_PLS = Net_MPD::factory('Playlist');
    $this->MPD_PLY = Net_MPD::factory('Playback');
    if (!$this->MPD_PLS->connect()) {
      die('Connection failed: '.print_r($this->MPD_DB->getErrors(), true));
    }
  }

  protected function echoJson($j) {
    header('Content-type: application/json');
    echo json_encode($j);    
  }

  protected function cmdNotFound() {
    $this->echojson(array("status"=>"bad", "result"=>"cmd not found."));
  }

  protected function getPlaylist() {
    $this->echoJson($this->MPD_PLS->getPlaylistInfo());
  }

  protected function getCurrentSong() {
    $this->echoJson($this->MPD_PLY->getCurrentSong());
  }

  protected function previousSong() {
    $this->echoJson($this->MPD_PLY->previousSong());
  }  

  protected function nextSong() {
    $this->echoJson($this->MPD_PLY->nextSong());
  }

  protected function stop() {
    $this->echoJson($this->MPD_PLY->stop());
  }  

  protected function pause() {
    $this->echoJson($this->MPD_PLY->pause());
  }

  protected function play() {
    $this->echoJson($this->MPD_PLY->play());
  }

  protected function playId($id) {
    $this->echoJson($this->MPD_PLY->playId($id));
  }

  protected function random($on) {
    $this->echoJson($this->MPD_PLY->random($on));
  }  

  protected function repeat($on) {
    $this->echoJson($this->MPD_PLY->repeat($on));
  }  

  protected function searchArtist($a) {
    $this->echojson($this->MPD_DB->find(array('Artist' => $a)));
  }

  protected function find($params, $caseSensitive=false) {
    $this->echojson($this->MPD_DB->find(array($params, $caseSensitive)));
  }  
  
  public function decodeRequest($r) {

    if(!isset($_REQUEST['cmd'])) {
      return $this->cmdNotFound();
    }

    switch($r['cmd']) {
      case "getCurrentSong":
        return $this->getCurrentSong();
      case "previousSong":
        return $this->previousSong();
      case "nextSong":
        return $this->nextSong();
      case "stop":
        return $this->stop();
      case "pause":
        return $this->pause();
      case "play":
        return $this->play();
      case "playId":
        return $this->playId($_REQUEST['id']);
      case "random":
      case "shuffle":
        return $this->random($_REQUEST['on']);
      case "repeat":
        return $this->repeat($_REQUEST['on']);
      case "getPlaylist":
        return $this->getPlaylist();
      case "searchArtist":
        return $this->searchArtist($_REQUEST['artist']);
      case "find":
        return $this->find($_REQUEST['params']);                
      default:
       return $this->cmdNotFound();
    }    
  }

//print_r($_REQUEST);

// Search for songs by Artist
// $dump = $MPD_DB->find(array('Artist' => 'Plump'));
// echo '<ol>';
// foreach ($dump as $song) {
//     echo '<li>'.$song['Title'].'</li>';
// }
// echo '</ol>';

// Get By Artist
// $dump = $MPD_DB->getMetaData('Artist');
// echo '<ol>';
// foreach ($dump as $artist) {
//     echo '<li>'.$artist.'</li>';
// }
// echo '</ol>';


}


$mpc=new mpdController();
$mpc->decodeRequest($_REQUEST);
