package com.bot;

import com.bot.TrackScheduler;
import com.sedmelluq.discord.lavaplayer.player.AudioPlayer;
import com.sedmelluq.discord.lavaplayer.track.AudioTrack;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.Matchers.any;
import static org.mockito.Matchers.eq;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.mock;


public class TrackSchedulerTest {

	private static TrackScheduler trackScheduler;
	private static AudioPlayer mockAudioPlayer = mock(AudioPlayer.class);
	private static AudioTrack mockAudioTrack = mock(AudioTrack.class);

	@Before
	public void setUp() {
		// Make new scheduler for each test
		trackScheduler = new TrackScheduler(mockAudioPlayer);
	}

	@Test
	public void testQueueTrack() {
		doReturn(true).when(mockAudioPlayer).startTrack(any(AudioTrack.class), eq(true));
		trackScheduler.queue(mockAudioTrack);

		assertEquals(mockAudioTrack, trackScheduler.getNowPlaying());
		assertEquals(0, trackScheduler.getNumQueuedTracks());

		// Now returns false since one track is playing
		doReturn(false).when(mockAudioPlayer).startTrack(any(AudioTrack.class), eq(true));
		trackScheduler.queue(mockAudioTrack);

		// Checks that song is added
		assertEquals(1, trackScheduler.getNumQueuedTracks());
	}

	@Test
	public void testStopPlayer() {
		doNothing().when(mockAudioPlayer).stopTrack();
		doReturn(true).when(mockAudioPlayer).startTrack(any(AudioTrack.class), eq(true));

		// Add initial track
		trackScheduler.queue(mockAudioTrack);

		// Adds tracks to queue
		doReturn(false).when(mockAudioPlayer).startTrack(any(AudioTrack.class), eq(true));
		trackScheduler.queue(mockAudioTrack);
		trackScheduler.queue(mockAudioTrack);
		trackScheduler.queue(mockAudioTrack);

		assertEquals(3, trackScheduler.getNumQueuedTracks());

		trackScheduler.stopPlayer();

		assertEquals(0, trackScheduler.getNumQueuedTracks());
		assertNull(trackScheduler.getNowPlaying());
	}

	@Test
	public void testNextTrack() {
		doNothing().when(mockAudioPlayer).stopTrack();
		doReturn(true).when(mockAudioPlayer).startTrack(any(AudioTrack.class), eq(true));

		// Add initial track
		trackScheduler.queue(mockAudioTrack);
		assertEquals(0, trackScheduler.getNumQueuedTracks());

		AudioTrack otherTrack = mock(AudioTrack.class);
		doReturn(false).when(mockAudioPlayer).startTrack(any(AudioTrack.class), eq(true));
		trackScheduler.queue(otherTrack);

		assertEquals(1, trackScheduler.getNumQueuedTracks());

		trackScheduler.nextTrack();
		assertEquals(0, trackScheduler.getNumQueuedTracks());
		assertEquals(otherTrack, trackScheduler.getNowPlaying());
	}
}
